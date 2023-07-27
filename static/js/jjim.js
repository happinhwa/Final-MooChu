function toggleWish(movieId, movieTitle) {
    const wishButton = document.getElementById('wish-btn');
    const nickname = wishButton.getAttribute('data-nickname');


    // AJAX 요청 보내기
    fetch(`/mypage/${nickname}/toggle_wish/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': '{{ csrf_token }}',
        },
        body: `movie_id=${movieId}&titleKr=${movieTitle}`,
    })
    .then(response => response.json())
    .then(data => {
        if (data.wished) {
            wishButton.innerText = '찜 취소';
            alert(`'${movieTitle}'이(가) 찜목록에 담겼습니다.`);
        } else { 
            wishButton.innerText = '찜하기';
        }
    })
    .catch(error => console.error('Error:', error));
}