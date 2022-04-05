function playVoice(word: string) {
    const audio = document.querySelector('#voice-player')
    audio.setAttribute('src', `http://localhost:37421/media/voices/${word}.mp3`)
}
