// page controller
var pageController = (function(coms) {
    // get data from the page
    var Comment = function(id, slide, main, level){
        this.id = id;
        this.slide = slide;
        this.main = main;
        this.level = level;
    };
    var data = {
        comments: [],
    };
    return {
        // get comments from the page
        getCommentsFromPage: function(){
            var rawComments = coms;
            var newCommentSet = [];
            for (var i in COMMENTS) {
                var id = rawComments[i]['pk'];
                var slide = rawComments[i]['fields']['slide'];
                var main = rawComments[i]['fields']['main'];
                var level = rawComments[i]['fields']['level'];
                var com = new Comment(id, slide, main, level);
                newCommentSet.push(com);
            }
            data.comments = newCommentSet;
            return data
        }
    }
})(COMMENTS);

// UI controllers
var UIController = (function() {
    var DOMS = {
        carouselA: '#carousel-a',
        carouselB: '#carousel-b',
        right: '.carousel-control-next',
        left: '.carousel-control-prev',
        lightbox: '.lightbox',
        close: '.closex',
        subchapters: '.controls',
        lazyLoad: '#lazyLoadLink',
        allComments: '#comments',
        singleComment: '.comment'
    };
    return {
        getDOMS: function(){
            return DOMS;
        }
    };
})();

// Lightbox controller
var lightboxController = (function(UIContr){
    
    DOM = UIContr.getDOMS();
    // set up eventListeners
    function setupEventlisteners(){
        // display on double click
        $(DOM.carouselB).on('dblclick', function(){ $(DOM.lightbox).show(); });
        // display on doubletouch
        $(DOM.carouselB).on('dblclick', function(){ $(DOM.lightbox).show(); });
        // close lightbox with ESC
        $(document).keydown(function(e) {
            if( e.keyCode === 27 ) {$(DOM.lightbox).hide(); }  
        });
        // close pressing cross
        $(DOM.close).click(function() {$(DOM.lightbox).hide(); })
    };
    return {
        init: function(){
            console.log('Lightbox control has started');
            setupEventlisteners();
        
        }
    };
        
})(UIController);

// Carousel controller

var carouselController = (function(UIContr){
    DOM = UIContr.getDOMS();

    // Sync carousels
    function syncCarousels() {
        // sync nav shevrons
        $(DOM.carouselB).on('click','a',function(){$(DOM.carouselA).carousel($(this).data('slide')); });
        $(DOM.carouselA).on('click','a',function(){$(DOM.carouselB).carousel($(this).data('slide')); });

        // add arrows control
        $(document)
            // highlight first link on load
            .ready(function(){
                if ($(DOM.subchapters).find("a").length) {
                    $(DOM.subchapters).find("a").eq(0).addClass("chosen");
                }
            })
            .keydown(function(e) {
                // if left arrow pressed
                if( e.keyCode === 37) {
                    $(DOM.carouselA).carousel('prev');
                    $(DOM.carouselB).carousel('prev');
                // if rigth arrow is pressed
                }  else if ( e.keyCode === 39) {
                    $(DOM.carouselA).carousel('next');
                    $(DOM.carouselB).carousel('next');
                }
            });
        // Change active color of the link and move both carousels
        $(DOM.subchapters).on('click','a',function(){
            // get slide destination
            var link = parseInt($(this).data('slide-to'));
            // check if another link is highlighted
            if($(".chosen").length){
                $(".chosen").removeClass('chosen')
            };
            $(this).addClass("chosen");

            // move carousels
            $(DOM.carouselA).carousel(link);
            $(DOM.carouselB).carousel(link);
        });
    };

    return {
        init: function(){
            console.log('carousel control has started');
            syncCarousels();
        }
    };
 
})(UIController)


var commentController = (function(pageCtrl, UIContr){
    var DOM = UIContr.getDOMS();
    var data = pageCtrl.getCommentsFromPage();
    // Collect info about page
    var page = {
        activeSlide: 0,
        allowedNumberOfComments: 2,
        step: 2,
        isLinkNeeded: function(active){
            var allActiveParents = $(DOM.singleComment).filter(function(){
                return $(this).data('slide') === active && $(this).data('level') === 0;
            }).get().length;

            if (allActiveParents > this.allowedNumberOfComments){
                return true;
            } else {
                return false;
            }
        },
        showLink: function(active){
            if (this.isLinkNeeded(active)){
                $(this.lazyLoadLink).show();
            } else {
                $(this.lazyLoadLink).hide();
            }
        },
        lazyLoadLink: DOM.lazyLoad,
        allComments: data.comments,
        hideAllComments: function(){ //choose and hide all comments 
            $(DOM.singleComment).each(function(){$(this).hide()});
        },
        displayAll: function(active){
            // get list of all related comments
            var allActive = $(DOM.singleComment).filter(function(){
                return $(this).data('slide') === active;
            });
            // selection of parent comments
            var mainSelection = allActive.filter(function(){
                return $(this).data('level') === 0;
            }).slice(0,this.allowedNumberOfComments);
            // get main attribute from parents to display their child comments
            var mains = mainSelection.map(function(){return $(this).data('main');}).get();
            // select children
            var childSelection = allActive.filter(function(){
                return $(this).data('level') > 0 && mains.includes($(this).data('main'));
            })
            mainSelection.show();
            childSelection.show();

        },
        //reset: function(){this.currentNumberOfComments = 2;},
        increase: function(){this.allowedNumberOfComments += this.step}
    };
    // catch changes in carousel index (active slide). MAIN trigger
    // event can be attached to only one carousel sinse the are synced
    function setMainTrigger(){
        // When slide method invoked
        $(DOM.carouselB).on('slide.bs.carousel', function () {
            page.hideAllComments();
        })
        // after change effect
        $(DOM.carouselB).on('slid.bs.carousel', function () {
            page.activeSlide = $(this).find(".active").index();
            page.displayAll(page.activeSlide);
            page.showLink(page.activeSlide);      
        });
        // click on lazy load link
        $(DOM.lazyLoad).click(function(){
            // increase allowed number
            page.increase();
            // show comments and decide weather link is needed again
            page.displayAll(page.activeSlide);
            page.showLink(page.activeSlide);

        });
    };
    return {
        init: function(){
            console.log('Comment control has started');
            // prepare comments
            page.hideAllComments();
            page.displayAll(0);
            page.showLink(0);
            // set event listeners
            setMainTrigger();
        },
        object: page
    };
})(pageController, UIController);



// INITIATE MODULES
jQuery(function($) {
    lightboxController.init();
    carouselController.init();
    commentController.init();
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
};})(jQuery);


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