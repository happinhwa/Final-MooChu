// static/js/main.js
$(document).ready(function() {
    loadMovies();  // 페이지 로딩 시 초기 데이터 로드
    
    $(window).scroll(function() {
        if ($(window).scrollTop() + $(window).height() >= $(document).height()) {
            loadMovies();  // 스크롤 이벤트 발생 시 추가 데이터 로드
        }
    });
});

function loadMovies() {
    $.ajax({
        url: '/load-more-data/',  // 데이터를 로드할 URL 설정
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            var movies = response.movies;
            var movieList = $('#movie-list');
            for (var i = 0; i < movies.length; i++) {
                var movie = movies[i];
                var imageElement = $('<img>')
                    .attr('src', movie.posterImageUrl)
                    .attr('alt', movie.title)
                    .addClass('movie-poster');
                movieList.append(imageElement);
            }
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}