document.addEventListener('DOMContentLoaded', function (e) {
    const form = document.getElementById('frmForm');
    const fv = FormValidation.formValidation(form, {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    obj: form.querySelector('[name="name"]').value,
                                    type: 'name',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El nombre del pais ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                proprietor: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                coordinates: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
            },
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
            submit_formdata_with_ajax_form(fv);
        });
});

$(function () {
    $('input[name="name"]').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });

    
    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    if (navigator.geolocation){
        navigator.geolocation.getCurrentPosition(getCoords, getError);
    }else{
        initMap(-0.9583194159319224,-78.61308148939898);

    }

    function getCoords(position){
        var lat = position.coords.latitude;
        var lng = position.coords.longitude;

        initMap(lat,lng);
    }

    function getError(err){
        initMap(-0.9585476347796161,-78.61304134393687);
    }

  
    function initMap(lat,lng) {
                  
        const myLatLng = new google.maps.LatLng(lat,lng);

        
        const map = new google.maps.Map(document.getElementById("mapa"), {
            zoom: 16,
            center: myLatLng
        });

        const marker = new google.maps.Marker({
            position: myLatLng,
            map,
            draggable: true,
            title: "Arrastrame a tu ubicación!"
        });

        const infowindow = new google.maps.InfoWindow({
            content: '<p>' + "{{ mainpage.name }}" + '</p>'
        });

      

        google.maps.event.addListener(marker,'position_changed',function() {
            getMarkerCoords(marker);
        });

    }

    $(function () {
        initMap();
    })
    
    function getMarkerCoords(marker){
        var markerCoords = marker.getPosition();
        $('#id_lat').val( markerCoords.lat() );
        $('#id_lng').val( markerCoords.lng() );

    }

});

