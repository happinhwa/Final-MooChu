// MovieList.js

import React, { useEffect, useState } from 'react';

function MovieList() {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    fetch('/api/movies/')  // Django에서 제공하는 영화 목록 API 엔드포인트로 변경해야 합니다.
      .then(response => response.json())
      .then(data => setMovies(data))
      .catch(error => console.error(error));
  }, []);

  return (
    <div className="container mt-3">
      <div className="row flex-row flex-nowrap overflow-auto">
        {movies.map((movie, index) => (
          <div className="col-lg-3 col-md-4 col-sm-6 mb-3" key={index}>
            <div className="card">
              {movie.img_link ? (
                <img className="poster lazyload lazyloaded" src={movie.img_link} alt={movie.title} />
              ) : (
                <img className="poster lazyload lazyloaded" src="/static/images/moochu.png" alt={movie.title} />
              )}
              <div className="card-body text-center">
                <h5 className="card-title">{movie.title}</h5>
                <p className="card-text d-day-label">D-{index + 1}</p>
                <p className="card-text">{movie.date}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default MovieList;
