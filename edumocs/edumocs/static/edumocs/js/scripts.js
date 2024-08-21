$(document).ready(function() {
    const csrfToken = $('#csrf-token').val();
    const enviarPreguntaUrl = $('#enviar-pregunta-url').val();

    $('#chat-message-submit').on('click', function() {
        let mensaje = $('#chat-message-input').val().trim();
        let preguntaId = $('#predefined-questions').val();

        if (preguntaId) {
            mensaje = $('#predefined-questions option:selected').text();
        }

        if (mensaje !== "") {
            $('#chat-log').append('<div><strong>Tú:</strong> ' + mensaje + '</div>');

            $.ajax({
                type: 'POST',
                url: enviarPreguntaUrl,
                data: {
                    'mensaje': mensaje,
                    'pregunta_id': preguntaId,
                    'csrfmiddlewaretoken': csrfToken
                },
                success: function(response) {
                    $('#chat-log').append('<div><strong>Respuesta:</strong> ' + response.respuesta + '</div>');
                    $('#chat-message-input').val('');
                    $('#predefined-questions').val('');
                },
                error: function(xhr, status, error) {
                    $('#chat-log').append('<div><strong>Error:</strong> No se pudo enviar la pregunta.</div>');
                }
            });
        }
    });
});
