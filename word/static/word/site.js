function playVoice(itemId) {
    var audio = document.querySelector('#voice-player');
    audio.setAttribute('src', "http://localhost:37421/media/voices/".concat(itemId, ".mp3"));
}
