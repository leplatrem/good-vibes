window.addEventListener('load', main);

async function main() {
  const player = new Player('player-view');
  player.queue = videos;

  const playlist = new Vue({
    el: '#playlist',
    data: {
      videos
    },
    methods: {
      play(video, e) {
        e.preventDefault();
        player.play(video);
      }
    }
  });

  await player.init();

  // Show currently playing song.
  player.addEventListener('playing', (e) => {
    const id = e.detail.id;
    const current = document.getElementsByClassName("playing");
    while (current.length) {
      current[0].classList.remove("playing");
    }
    document.getElementById(`video-${id}`).classList.add("playing");
  });

  player.playNext();
}


class Player {
  constructor(elt) {
    this.el = document.getElementById(elt);
    // Use its DOM element to dispatch events.
    this.addEventListener = this.el.addEventListener.bind(this.el);

    // https://plyr.io instance.
    this.plyr = null;

    this.queue = [];
  }

  async init() {
    // Setup plry in DOM.
    this.plyr = plyr.setup(this.el, {
      controls: ['play-large', 'play', 'progress', 'current-time', 'mute', 'volume', 'airplay', 'fullscreen'],
    })[0];
    // Wait for initialization.
    await new Promise((resolve) => this.plyr.on('ready', resolve));
    // Play when video is loaded.
    this.plyr.on('ready', () => this.plyr.togglePlay(true));
    // Play next when current ends.
    this.plyr.on('ended', () => this.playNext());
    // Play next when error occurs.
    this.plyr.on('error', (e) => {
      console.error('skip, will play next', e);
      this.playNext();
    });
  }

  play(video) {
    // Truncate queue starting from this video.
    const idx = this.queue.findIndex(({ id }) => video.id == id);
    this.queue = this.queue.slice(idx + 1);

    // Load video into player. Will eventually fire 'ready'.
    const { id, type = "youtube", title = "" } = video;
    this.plyr.source({
      type: 'video',
      title: title,
      sources: [{ src: id, type }]
    });
    // Notify that video was loaded.
    this.el.dispatchEvent(new CustomEvent('playing', { detail: video }));
  }

  playNext() {
    if (this.queue.length > 0) {
      this.play(this.queue[0]);
    } else {
      // Nothing to play.
      this.plyr.pause();
    }
  }
}
