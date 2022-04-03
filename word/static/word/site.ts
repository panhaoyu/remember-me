function playVoice(itemId: number) {
    const audio = document.querySelector('#voice-player')
    audio.setAttribute('src', `http://localhost:37421/media/voices/${itemId}.mp3`)
}
