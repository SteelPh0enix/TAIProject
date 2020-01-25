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
                toggle_vote_button(id);
            } else {
                alert(`Something went wrong while changing a vote: ${data['reason']}`)
            }
        });
}

function delete_spectrogram(id) {
    fetch(`/spectrogram/${id}/delete`)
    .then(response => response.json())
    .then(data => {
        if (data['status'] === 'OK') {
            location.reload();
        } else {
            alert(`Something went wrong while deleting spectrogram: ${data['reason']}`);
        }
    });
}