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

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function edit_spectrogram(id, new_title) {
    fetch(`/spectrogram/edit`, {
            method: 'POST',
            mode: 'same-origin',
            credentials: 'include',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'id': id, 'title': new_title })
        }).then(response => response.json())
        .then(data => {
            if (data['status'] === 'OK') {
                location.reload();
            } else {
                alert(`Something went wrong while editing spectrogram: ${data['reason']}`);
            }
        })
}