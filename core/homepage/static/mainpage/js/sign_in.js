var fv;
var input_birthdate;
var date_current;
var select_parish;
var pathname = window.location.pathname;

document.addEventListener('DOMContentLoaded', function (event) {
    const form = document.getElementById('frmLogin');
    const submitButton = form.querySelector('[type="submit"]');
    fv = FormValidation.formValidation(form, {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                // defaultSubmit: new FormValidation.plugins.DefaultSubmit(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                first_name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                      
                    }
                },
                last_name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                      
                    }
                },
                dni: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 10,
                        },
                        digits: {},
                        remote: {
                            url: pathname,
                            // Send { username: 'its value', email: 'its value' } to the back-end
                            data: function () {
                                return {
                                    obj: form.querySelector('[name="dni"]').value,
                                    type: 'dni',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El número de cedula ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                email: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 5
                        },
                        regexp: {
                            regexp: /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/i,
                            message: 'El email no es correcto'
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    obj: form.querySelector('[name="email"]').value,
                                    type: 'email',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El email ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                image: {
                    validators: {
                        file: {
                            extension: 'jpeg,jpg,png',
                            type: 'image/jpeg,image/png',
                            maxFiles: 1,
                            message: 'Introduce una imagen válida'
                        }
                    }
                },
                gender: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un genero',
                        },
                    }
                },
                mobile: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 10
                        },
                        digits: {},
                        remote: {
                            url: pathname,
                            // Send { username: 'its value', email: 'its value' } to the back-end
                            data: function () {
                                return {
                                    obj: form.querySelector('[name="mobile_phone"]').value,
                                    type: 'mobile',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El número de teléfono ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                phone: {
                },
                address: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 4,
                        }
                    }
                },
                birthdate: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
                    }
                },
                district: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un Barrio',
                        },
                    }
                }
            }
        }
    )
        .on('core.element.validated', function (e) {
            if (e.valid) {
                const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                if (groupEle) {
                    FormValidation.utils.classSet(groupEle, {
                        'has-success': false,
                    });
                }
                FormValidation.utils.classSet(e.element, {
                    'is-valid': false,
                });
            }
            const iconPlugin = fv.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var form = fv.form;
            var parameters = new FormData($(form)[0]);
            parameters.append('action', 'add');
            submit_formdata_with_ajax('Notificación', '¿Estas seguro de registrarse?', pathname, parameters, function () {
                alert_sweetalert('success', 'Alerta', 'Se ha registrado correctamente en nuestro sitio web. Se le ha enviado un correo donde estaran sus credenciales', function () {
                    location.href = fv.form.getAttribute('data-url');
                }, null, null)
            });
        });
});

$(function () {

    input_birthdate = $('input[name="birthdate"]');
    date_current = new moment().format("YYYY-MM-DD");
    select_district = $('select[name="district"]');

    console.log('fecha', date_current);
    input_birthdate.datetimepicker({
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        defaultDate: "2007-01-01",
        maxDate: "2007-01-01"
    });

    input_birthdate.datetimepicker('date', input_birthdate.val());

    input_birthdate.on('change.datetimepicker', function (e) {
        fv.revalidateField('birthdate');
    });

    $('input[name="dni"]').keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    $('input[name="first_name"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });

    $('input[name="last_name"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });

    $('input[name="mobile"]').keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    $('input[name="phone"]').keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    $('select[name="gender"]').on('change.select2', function () {
        fv.revalidateField('gender');
    });

    select_district.select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            url: pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_district'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
    })
        .on('select2:select', function (e) {
            console.log(e.params.data);
            fv.revalidateField('parish');
        })
        .on('select2:clear', function (e) {
            fv.revalidateField('parish');
        });

    // $(fv.form).find('input[name="first_name"]').val('Oscar Alberto');
    // $(fv.form).find('input[name="last_name"]').val('Pinos Almeida');
    // $(fv.form).find('input[name="dni"]').val('0913960944');
    // $(fv.form).find('input[name="mobile"]').val('0979014552');
    // $(fv.form).find('input[name="phone"]').val('2977552');
    // $(fv.form).find('input[name="password"]').val('hacker94');
    // $(fv.form).find('input[name="address"]').val('Milagro');
    // $(fv.form).find('select[name="parish"]').val('549').trigger('change.select2');
    // $(fv.form).find('input[name="email"]').val('williamjairdavilavargas@gmail.com');
});