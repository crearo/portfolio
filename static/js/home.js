$(function() {
  /* NOTE: hard-refresh the browser once you've updated this */
  $(".typed").typed({
    strings: [
      "stat peterparker<br/>" +
      "><span class='caret'>$</span> job: Friendly Neighborhood Spider-Man<br/> ^100" +
      "><span class='caret'>$</span> skills: combat spider, villain slayer<br/> ^100" +
      "><span class='caret'>$</span> hobbies: star-gazer, universe whisperer, mountain-biker<br/> ^300" +
      "><span class='caret'>$</span> alias: spiderman<br/> ^300" +
      "><span class='caret'>$</span> universe: found traces in every universe<br/> ^300"
    ],
    showCursor: true,
    cursorChar: '_',
    autoInsertCss: true,
    typeSpeed: 0.001,
    startDelay: 50,
    loop: false,
    showCursor: false,
    onStart: $('.message form').hide(),
    onStop: $('.message form').show(),
    onTypingResumed: $('.message form').hide(),
    onTypingPaused: $('.message form').show(),
    onComplete: $('.message form').show(),
    onStringTyped: function(pos, self) {$('.message form').show();},
  });
  $('.message form').hide()
});
