$(function() {
  $(".typed").typed({
    strings: [
      "Oops! <br/>" + 
      "><span class='caret'>$</span> You might have mis-typed the URL, <br/> ^1" +
      "><span class='caret'>$</span> or maybe the page has been moved. <br/> ^500" +
      "><span class='caret'>$</span> Anyways, there is nothing to see here... <br/> ^1000" +
      "><span class='caret'>$</span> Would you like to go back to the <a href='#'>homepage</a>?"
    ],
    showCursor: true,
    cursorChar: '_',
    autoInsertCss: true,
    typeSpeed: 30,
    startDelay: 200,
    loop: false,
    showCursor: false,
    onStart: $('.message form').hide(),
    onStop: $('.message form').show(),
    onTypingResumed: $('.message form').hide(),
    onTypingPaused: $('.message form').show(),
    onComplete: $('.message form').show(),
    onStringTyped: $('.message form').show()
  });
  $('.message form').hide()
});