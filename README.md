# Virtual Christmas Cards

I sorta stole [Ayush's idea](https://github.com/Shad0wSeven/christmas2021) here, but with a few modifications. This is how I sent my virtual christmas cards for 2022!

The opening page provides a password input box:
![opening](https://media.discordapp.net/attachments/962420061958709288/1055252153746337912/Screenshot_2022-12-21_at_2.35.13_PM.png?width=1410&height=897)

When you click the button, the page 'loads' with a little js:

```js
function goButton() {
  let submission = document.getElementById("pwd").value;
  if (submission.length > 0) {
    document.getElementById("abovetext").innerHTML = 'unlocking..';
    console.log(document.getElementById("abovetext").innerHTML);

    document.getElementById("abovetext").classList.add("italic")

    const time = 4000;
    const periods = 6;
    setTimeout(function(){ window.location.href = "/" + submission.toLowerCase() + ".html"}, time);
    for (let x = 0; x < periods; x++) {
      setTimeout(() => {
        document.getElementById("abovetext").innerHTML = document.getElementById("abovetext").innerHTML + '.';
      }, x * (time / periods))
    }

    console.log("pwd accepted")

  }
}

```

Which changes the 'Enter secret password' text to 'unlocking...' with incrementing dots.

If the password is rejected, it redirects back to the page with an 'invalid' code:

![invalid](https://media.discordapp.net/attachments/962420061958709288/1055252940706828350/Screenshot_2022-12-21_at_2.38.21_PM.png?width=1410&height=897)

With a slight chance of redirecting you to a video of Buddy the Elf:

```js
let url = new URL(window.location.href)
let params = new URLSearchParams(url.search)
let error = params.get("error")
if (error == 1) {
  document.getElementById("invalidcode").innerHTML = 'invalid... 😡';
  document.getElementById("pwd").value = '';

  if (Math.round(Math.random() * 10) % 2 == 0) {
    setTimeout(function(){ window.location.href = "https://www.youtube.com/watch?v=DTF_K5D7jX8"}, 500);
  }
}
```

But if you enter the right password, then you get redirected to the card:

![card](https://media.discordapp.net/attachments/962420061958709288/1055252099983736842/Screenshot_2022-12-21_at_2.34.43_PM.png?width=1410&height=897)

With [confetti](https://www.npmjs.com/package/js-confetti)!

```js
let jsConfetti = new JSConfetti();

function playConfetti(emojis) {
  jsConfetti.addConfetti({
    emojis: emojis,
    emojiSize: 100,
    confettiNumber: 30,
    confettiColors: [
      "#ff0a54",
      "#ff477e",
      "#ff7096",
      "#ff85a1",
      "#fbb1bd",
      "#f9bec7",
    ],
  });
};

function playInput() {
  input = document.getElementById("title").innerHTML;
  if (input != "🎄🎄 Merry Christmas! 🎄🎄") {

    let emojis = [];
    let counter = 0;
    let completeCharacter = "";
    for (let x = 0; x < input.length; x++) {
      completeCharacter += input.substring(x, x + 1);
      if (x % 2 == 1) {
        emojis[counter] = completeCharacter;
        completeCharacter = "";
        counter++;
      }
    }
    console.log(emojis);
    playConfetti(emojis);
  }
  else {
    playConfetti(["🎄", "🎅🏼", "🎁"]);
  }
}
```

The 'Click me!' button replays the animation, but you can play your own emojis by replacing the title text box:

![emojis](https://media.discordapp.net/attachments/962420061958709288/1055255177956958288/Screenshot_2022-12-21_at_2.47.10_PM.png?width=1410&height=897)

Also, music will start playing in the background (unless you're in safari, which blocks autoplay)

```js
<audio id="music" autoplay loop src="{{music}}" type="audio/mp3"></audio>
```

And that's about it!

### More cool stuff!

The password is technically the title of a subpage - the `goButton()` function that checks the password is actually just redirecting to [entered_password].html, and if that doesn't exist, the 404 page redirects back to the index.

That means that each letter has it's own subpage which is... practically identical, except for the text body, which is customized.

Since I made a lot of letters this year, I wanted a way to consolidate the format of the letters in a single html file which could be easily edited for changes to the theme. My solution was to make a text file for each letter with some jekyll-themed front matter to configure the music preference for each letter. 

Example.txt: 
```
---
music: /music/elf.mp3
---
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam mattis neque eu ligula 
```

`build.py` generates the html file for each letter by copying `letter-layout.html` and replacing the configurable elements (which are in double curly brackets i.e. `{{text_body}}`). The newly generated files are placed in `/dist/`, and this is what is actually deployed.

`deploy.sh` is a convenient deployment script to build, commit, and push the files. 
