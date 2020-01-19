'use strict';

function toggle_vote_button(id) {
    let button = document.getElementById(`fav-btn-${id}`)

    button.classList.toggle('spectrum-fav-used')
    fetch(`/spectrogram/${id}/votes`)
        .then(response => response.json())
        .then(data => {
            button.innerHTML = `&#9733; ${data['votes']}`
        });
}

function toggle_vote(id) {
    fetch(`/spectrogram/${id}/toggle_fav`)
        .then(response => response.json())
        .then(data => {
            if (data['status'] === 'OK') {
                toggle_vote_button(id)
            } else {

            }
        });
}