from django.conf import LazySettings
from django.forms import FileInput, forms
from django.utils.safestring import mark_safe

settings = LazySettings()


class BootstrapFileInput(FileInput):
    # bootstrap = {
    #     'append': mark_safe('<i class="icon-calendar"></i>'),
    #     'prepend': None,
    # }

    # @property
    # def media(self):
    #     js = (
    #         settings.STATIC_URL + '/js/bootstrap/plugins/bootstrap-fileupload.js',
    #     )
    #     css = {
    #         'screen': (
    #             settings.STATIC_URL + '/css/bootstrap/plugins/bootstrap-fileupload.css',
    #         )
    #     }
    #     return forms.Media(css=css, js=js)

    def render(self, name, value, attrs=None):
        pre = """<div class='fileupload fileupload-new' data-provides='fileupload'>
                    <div class='input-append'>
                        <div class='uneditable-input span3'>
                            <i class='icon-file fileupload-exists'></i>
                            <span class='fileupload-preview'></span>
                        </div>
                <span class='btn btn-file'>
                    <span class='fileupload-new'>Select file</span>
                    <span class='fileupload-exists'>Change</span>
                """
        post = """
                </span>
                        <a href='#' class='btn fileupload-exists' data-dismiss='fileupload'>Remove</a>
                    </div>
                </div>
                """
        return mark_safe(pre) + super(BootstrapFileInput, self).render(name, value, attrs=attrs) + mark_safe(post)
