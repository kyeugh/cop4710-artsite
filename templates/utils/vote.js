$(".vote-button").click(function() {
    var button = $(this);
    var slug = button.attr("name");
    $.ajax({
        type: "POST",
        url: "{% url 'vote' %}",
        data: {
            "slug": slug,
            "csrfmiddlewaretoken": "{{ csrf_token }}"
        },
        dataType: "json",
        success: function(response) {
            $(".vote-button-" + slug).each(function (index, element) {
                $(this).toggleClass("liked");
            })
            $(".votes-" + slug).each(function (index, element) {
                $(this).text(response.votes_count);
            })
        },
        error: function(rs, e) {
            alert(rs.response_text)
        }
    })
});