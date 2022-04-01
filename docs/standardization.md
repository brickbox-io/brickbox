# Standardization

## Templates

When working with HTML pages, it is often necessary to standardize the structure of the page. This is done by using the [Django template system](https://docs.djangoproject.com/en/4.0/topics/templates/). There are currently two distinct sources (apps) for templates:

* bb_public
* bb_dashboard

Templates are created using the following conventions:

* \<AppName>_base.html
  * \<AppName>_header.html
  * \<AppName>_footer.html

The base template includes the header and footer, while all other pages extend from the base page.
