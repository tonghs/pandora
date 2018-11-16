var setFrameSize;

setFrameSize = function() {
  $('iframe#main-frame').height($('.content-wrapper').height());
  $('iframe#main-frame').width($('.content-wrapper').width());
};

$(document).ready(function() {
  $(window).resize(function() {
    setFrameSize();
  });
  setTimeout(function() {setFrameSize();}, 500);
});
