var btn = document.getElementById('fullscreen');
var carousel = document.getElementById('carousel-b');
var lightbox = document.querySelector('.lightbox');

// Display lightbox
btn.addEventListener('click', function(){
    console.log('click on button');

    lightbox.style.display = 'block';
    
})
carousel.addEventListener('dblclick', function(){
    console.log('double click');

    lightbox.style.display = 'block';
    
})

var area = document.querySelector('.lightbox');

area.addEventListener('click', function(e) {
    // check if we click around picture
    if (e.target.className === 'lightbox'){
        lightbox.style.display = 'none';
    }
})

// Sync slider
$('#carousel-b').on('click','a',function(){
    var other = 'a';
    $('#carousel-' + other).carousel(this.getAttribute('data-slide'));

})

$('#carousel-a').on('click','a',function(){
    var other = 'b';
    $('#carousel-' + other).carousel(this.getAttribute('data-slide'));

})

// Sync controls

var $controls = $('.controls');

$controls.on('click','a',function(e){
    var link = this.getAttribute('data-slide-to');
    console.log(this.getAttribute('data-slide-to'));
    $('#carousel-a').carousel(parseInt(link));
    $('#carousel-b').carousel(parseInt(link));
    
    ;
})
