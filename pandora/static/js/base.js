var setFrameSize;

setFrameSize = function() {
  setTimeout(function() {
    $('iframe#main-frame').animate({'height': $('.content-wrapper').height()}, 100);
    $('iframe#main-frame').animate({'width': $('.content-wrapper').width()}, 100);
  }, 500);
};

$(document).ready(function() {
  $(window).resize(function() {
    setFrameSize();
  });
  setFrameSize();
});
