


var facebook ={
    url : window.location.href,
    metaUrl : function() {
        $("#meta-url-fb").attr("content", this.url);
    },
    activeImgUrl: function(){ return $('#carousel-b .active').find('img')[0].src },
    metaImg : function() {
        $("#meta-img-fb").attr("content", this.activeImgUrl)
    }
}
// update link on load For facebook
window.onload = facebook.metaUrl();
window.onload = facebook.metaImg();


//var carousel = document.getElementById('carousel-b');
var lightbox = document.querySelector('.lightbox');

// Display lightbox
$('#carousel-b').on('dblclick', function(){
    console.log('double click');

    lightbox.style.display = 'block';
    
})
// close lightbox with ESC
$(document).keydown(function(e) {
    if( e.keyCode === 27 ) {
        lightbox.style.display = 'none';
    }
});
// close pressing cross
$('.closex').click(function(e) {
    lightbox.style.display = 'none';
})
    
// Sync slider
$('#carousel-b').on('click','a',function(e){
        lazyLoad.displayOnly(nextPrev(e, 'b'))
        lazyLoad.linkAction(nextPrev(e, 'b'))
        var other = 'a';
        $('#carousel-' + other).carousel(this.getAttribute('data-slide'));
    });
// update facebook meta
// facebook.metaImg();





$('#carousel-a').on('click','a',function(e){
    lazyLoad.displayOnly(nextPrev(e, 'a'))
    lazyLoad.linkAction(nextPrev(e, 'a'))
    var other = 'b';
    $('#carousel-' + other).carousel(this.getAttribute('data-slide'));
    // // update facebook meta
    // facebook.metaImg();
})


// Sync controls

$('.controls').on('click','a',function(e){
    var link = parseInt(this.getAttribute('data-slide-to'));
    lazyLoad.displayOnly(link);
    lazyLoad.linkAction(link);

    // change active color
    if($(".chosen").length){
        $(".chosen")[0].classList.remove('chosen')
    };

    this.classList.add("chosen");


    $('#carousel-a').carousel(link);
    $('#carousel-b').carousel(link);

    // update facebook meta
    facebook.metaImg();
});
// add color to A after load

$(document).ready(function() {
    if ($('.controls').find("a").length) {
        $('.controls').find("a")[0].classList.add("chosen");
      //  $('.controls').parent().find("#chapter-link")[0].classList.add("chosen-main");
    }
});

// move carousel from comments link

// $('#comments').on('click','a',function(e){
//     var link = this.getAttribute('data-slide-to');
//     console.log(this.getAttribute('data-slide-to'));
//     $('#carousel-a').carousel(parseInt(link));
//     $('#carousel-b').carousel(parseInt(link));
// });

function activeSlide(){
    var activeSlide = $('#carousel-b .active').index();
    return activeSlide
};
// check if we go next of back
function nextPrev(e, carousel){
    var className = e.currentTarget.className;
    var active = activeSlide();
    console.log('active is ' +active);
    var numberOfSlides = $('#carousel-' + carousel).find('.item').length - 1;
    console.log('# of slides ' + numberOfSlides );
    if (className === 'carousel-control-next'){
        if (active === numberOfSlides){
            return 0;
        } else{
            return active + 1;
        };
    } else if (className === 'carousel-control-prev'){
        if (active === 0){
            return numberOfSlides;
        } else{
            return active - 1;
        };
    }
};

// check slides on load
window.onload = function() {
    lazyLoad.displayOnly(0);
    lazyLoad.linkAction(0);
}

// Load more 
var lazyLoad ={
    allowedNumber: 2,
    step: 2,
    currentNumber: 2,
    activeSlide: 0,
    link: $('#lazyLoadLink'),
    // hide or show link based on its status
    linkAction: function(slide){ 
        if(this.status(slide)){ 
            this.link.hide();
            this.reset();
        } else {
            this.link.show();
        };
    }, 
    status: function(slide){
        // return true if link is needed
        var result = (this.totalNumberOfCommentsX(slide) <= this.currentNumber) ?  true :  false;
        return result
    } ,
    reset: function(){
        this.currentNumber = 2;
    },
    increase: function(){
        this.currentNumber += this.step;
    },
    totalNumberOfComments: function(){
        return $( ".comment").length;
    },
    totalNumberOfCommentsX: function(slide){
        return $(".container[data-slide='" + slide + "']").filter(function(){return $(this).data('level') === 0 }).length;
    },
    displayOnly: function(slide) {
        var $allContainers = $( ".comment")
        var display = [];
        for (i = 0; i < $allContainers.length; i++){
            $allContainers[i].style.display = 'none';
            if (parseInt($allContainers[i].dataset.slide) == slide) {
                display.push($allContainers[i])
                //$allContainers[i].style.display = 'block';
            }; 
        };
        // display only withing range
        // check if the list long enough
        var onlyMain = display.filter(function(el){return el.getAttribute('data-level') == 0 });        
        var number = (onlyMain.length <  this.currentNumber) ? onlyMain.length : this.currentNumber;

        //
        for (i = 0; i < number; i++){
            // idea : find main comments. display only two main comments with threads
            let main_id = onlyMain[i].getAttribute('data-main');            
            let toShow = display.filter(function(el){return el.getAttribute('data-main') === main_id} );          
            toShow.forEach(function(el){el.style.display = 'block'});
        
        };
    }
};

// Manage lazy load link
$('#lazyLoadLink').on('click', function(){
    lazyLoad.increase();
    lazyLoad.displayOnly(activeSlide());
    lazyLoad.linkAction(activeSlide());
});

// double tap
(function($){

    $.event.special.doubletap = {
      bindType: 'touchend',
      delegateType: 'touchend',
  
      handle: function(event) {
        var handleObj   = event.handleObj,
            targetData  = jQuery.data(event.target),
            now         = new Date().getTime(),
            delta       = targetData.lastTouch ? now - targetData.lastTouch : 0,
            delay       = delay == null ? 300 : delay;
  
        if (delta < delay && delta > 30) {
          targetData.lastTouch = null;
          event.type = handleObj.origType;
          ['clientX', 'clientY', 'pageX', 'pageY'].forEach(function(property) {
            event[property] = event.originalEvent.changedTouches[0][property];
          })
  
          // let jQuery handle the triggering of "doubletap" event handlers
          handleObj.handler.apply(this, arguments);
        } else {
          targetData.lastTouch = now;
        }
      }
    };
  
  })(jQuery);

  // doubletouch
  $('#carousel-b').on('doubletap',function(e){
        lightbox.style.display = 'block';
    });

    //////// COLOR PALETTE /////////
    
    $("#full").spectrum({
        color: "#ECC",
        showInput: true,
        className: "full-spectrum",
        showInitial: true,
        showPalette: true,
        showSelectionPalette: true,
        maxSelectionSize: 10,
        preferredFormat: "hex",
        localStorageKey: "spectrum.demo",
        move: function (color) {
            
        },
        show: function () {
        
        },
        beforeShow: function () {
        
        },
        hide: function () {
        
        },
        change: function() {
            
        },
        palette: [
            ["rgb(0, 0, 0)", "rgb(67, 67, 67)", "rgb(102, 102, 102)",
            "rgb(204, 204, 204)", "rgb(217, 217, 217)","rgb(255, 255, 255)"],
            ["rgb(152, 0, 0)", "rgb(255, 0, 0)", "rgb(255, 153, 0)", "rgb(255, 255, 0)", "rgb(0, 255, 0)",
            "rgb(0, 255, 255)", "rgb(74, 134, 232)", "rgb(0, 0, 255)", "rgb(153, 0, 255)", "rgb(255, 0, 255)"], 
            ["rgb(230, 184, 175)", "rgb(244, 204, 204)", "rgb(252, 229, 205)", "rgb(255, 242, 204)", "rgb(217, 234, 211)", 
            "rgb(208, 224, 227)", "rgb(201, 218, 248)", "rgb(207, 226, 243)", "rgb(217, 210, 233)", "rgb(234, 209, 220)", 
            "rgb(221, 126, 107)", "rgb(234, 153, 153)", "rgb(249, 203, 156)", "rgb(255, 229, 153)", "rgb(182, 215, 168)", 
            "rgb(162, 196, 201)", "rgb(164, 194, 244)", "rgb(159, 197, 232)", "rgb(180, 167, 214)", "rgb(213, 166, 189)", 
            "rgb(204, 65, 37)", "rgb(224, 102, 102)", "rgb(246, 178, 107)", "rgb(255, 217, 102)", "rgb(147, 196, 125)", 
            "rgb(118, 165, 175)", "rgb(109, 158, 235)", "rgb(111, 168, 220)", "rgb(142, 124, 195)", "rgb(194, 123, 160)",
            "rgb(166, 28, 0)", "rgb(204, 0, 0)", "rgb(230, 145, 56)", "rgb(241, 194, 50)", "rgb(106, 168, 79)",
            "rgb(69, 129, 142)", "rgb(60, 120, 216)", "rgb(61, 133, 198)", "rgb(103, 78, 167)", "rgb(166, 77, 121)",
            "rgb(91, 15, 0)", "rgb(102, 0, 0)", "rgb(120, 63, 4)", "rgb(127, 96, 0)", "rgb(39, 78, 19)", 
            "rgb(12, 52, 61)", "rgb(28, 69, 135)", "rgb(7, 55, 99)", "rgb(32, 18, 77)", "rgb(76, 17, 48)"]
        ]
    });

//// slide to right reply

//$('body,html').animate({scrollTop:$('div#comment-form').offset().top},500)
$('#comments').on('click','#replied-to',function(e){
    e.preventDefault();
    let id = $(this).data('replied-to')
    $('body,html').animate({scrollTop:$('.comment#'+id).offset().top},{
        queue: true,
        duration: 300
      })
    });