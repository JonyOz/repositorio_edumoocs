$(document).ready(function() {
    const csrfToken = $('#csrf-token').val();

    // Manejar el clic en una notificación para cargar la pregunta en la sección de respuesta
    $('.notificacion-item').on('click', function(e) {
        e.preventDefault();
        const preguntaId = $(this).data('id');
        const preguntaMensaje = $(this).text();

        // Mostrar la pregunta seleccionada
        $('#pregunta-seleccionada').text(preguntaMensaje);
        $('#respuesta-seccion').show();

        // Configurar el botón de respuesta
        $('#respuesta-submit').off('click').on('click', function() {
            const respuesta = $('#respuesta-input').val();

            if (respuesta.trim() !== "") {
                $.ajax({
                    type: 'POST',
                    url: `/responder/${preguntaId}/`,  // URL que incluye el ID de la pregunta
                    data: {
                        'respuesta': respuesta,
                        'csrfmiddlewaretoken': csrfToken
                    },
                    success: function(response) {
                        if (response.success) {
                            alert('Respuesta enviada correctamente.');
                            $('#respuesta-input').val('');
                            $('#respuesta-seccion').hide();
                        } else {
                            alert('Error al enviar la respuesta.');
                        }
                    },
                    error: function(xhr, status, error) {
                        alert('Hubo un error al enviar la respuesta.');
                    }
                });
            } else {
                alert('Por favor, escribe una respuesta.');
            }
        });
    });
});
