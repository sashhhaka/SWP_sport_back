(function ($) {
    $('.status-toggle').change(function () {
        var selectedOption = $(this).val();
        var url = $(this).data('url');
        $.ajax({
            url: url,
            type: 'POST',
            data: {
                csrfmiddlewaretoken: '{{ csrf_token }}',
                status: selectedOption,
            },
            success: function () {
                alert('Status updated successfully.');
            },
            error: function () {
                alert('An error occurred while updating the status.');
            }
        });
    });
})(django.jQuery);
