''' Tasks that support overall system operations. '''

from celery import shared_task
import box

from bb_vm.models import GPU, BackgroundTask


@shared_task
def prepare_gpu_background_task():
    '''
    Cycles through available GPUs to confirm all have background VM ready to launch.
    '''
    gpu_list = GPU.objects.all()
    for gpu in gpu_list:
        if not gpu.bg_ready and not gpu.rented and gpu.host.is_ready:
            host = gpu.host

            background_brick = box.Brick(host_port=host.ssh_port, brick_id=f'gpu_{str(gpu.id)}')
            background_brick.USER_DATA = BackgroundTask.objects.all().order_by('-id')[0].script     # pylint: disable=C0103

            background_brick.create(base_image="base_os-1")
            background_brick.set_root_password(password='r0flduqu')
            background_brick.attach_gpu(xml_data=f'{str(gpu.xml)}')
            background_brick.toggle_state(set_state='on')

            gpu.bg_ready = True
            gpu.bg_running = True
            gpu.save()

@shared_task
def stop_bg(gpu_id):
    '''
    Called to stop the background img for a particular GPU.
    '''
    gpu = GPU.objects.get(id=gpu_id)
    host = gpu.host

    background_brick = box.Brick(host_port=host.ssh_port, brick_id=f'gpu_{str(gpu.id)}')
    background_brick.toggle_state(set_state="off")

    gpu.bg_running = False
    gpu.save()


@shared_task
def start_bg():
    '''
    Called to start the background img for a particular GPU.
    '''
    gpu_list = GPU.objects.all()
    for gpu in gpu_list:
        if gpu.bg_ready and not gpu.rented and gpu.host.is_ready and not gpu.bg_running:
            host = gpu.host

            background_brick = box.Brick(host_port=host.ssh_port, brick_id=f'gpu_{str(gpu.id)}')
            background_brick.toggle_state(set_state="on")

            gpu.bg_running = True
            gpu.save()
