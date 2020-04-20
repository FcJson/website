(function ($) {
    "use strict";
 
    /*-------------------------------------
        Animation on scroll: Number rotator
    -------------------------------------*/
    $("[location-appear-animation]").each(function() {
        var self      = $(this);
        var animation = self.data("appear-animation");
        var delay     = (self.data("appear-animation-delay") ? self.data("appear-animation-delay") : 0);        

        if( $(window).width() > 959 ) { 
            self.html('0');
            self.waypoint(function(direction) {
                if( !self.hasClass('completed') ){
                    var from     = self.data('from');
                    var to       = self.data('to');
                    var interval = self.data('interval');
                    self.numinate({
                        format: '%counter%',
                        from: from,
                        to: to,
                        runningInterval: 2000,
                        stepUnit: interval,
                        onComplete: function(elem) {
                            self.addClass('completed');
                        }
                    });
                }
            }, { offset:'85%' });
        } else {
          self.html(self.data('to'));
        }
    });

    /*-------------------------------------
    SlickSlider
    -------------------------------------*/
       var slickslider = $(".slick-carousel");
       slickslider.each(function () {
            var $this = $(this),
                $items = ($this.data('items')) ? $this.data('items') : 1, 
                $navdots = ($this.data('dots')) ? $this.data('dots') : false,
                $navarrow = ($this.data('arrows')) ? $this.data('arrows') : false,
                $autoplay = ($this.attr('location-autoplay')) ? $this.data('autoplay') : true,
                $d_show = ($this.attr('location-slides')) ? $this.data('slides') : 3,
                $t_show = ($this.attr('location-tslides')) ? $this.data('tslides') : 2,
                $i_show = ($this.attr('location-islides')) ? $this.data('islides') : 1;
                

                $this.slick({
                  dots: $navdots,
                  infinite: false,
                  arrows:$navarrow,
                  autoplay: $autoplay, 
                  speed: 300, 
                  slidesToShow: $d_show,
                  slidesToScroll: 1,
                  responsive: [
                    {
                      breakpoint: 1024,
                      settings: {
                        slidesToShow: $t_show,
                        slidesToScroll: 1,
                      }
                    },
                    {
                      breakpoint: 600,
                      settings: {
                        slidesToShow: $i_show,
                        slidesToScroll: 1
                      }
                    },
                    {
                      breakpoint: 480,
                      settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1
                      }
                    }
                  ]
                });
          });

    /*-------------------------------------
    ProgressBar
    -------------------------------------*/
      var $progressBar = $('.skill-bar');
            $progressBar.each(function (i, elem) {
                var $elem = $(this),
                    percent = $elem.attr('location-percent') || "100",
                    delay = $elem.attr('location-delay') || "100",
                    type = $elem.attr('location-type') || "%";

                if (!$elem.hasClass('progress-animated')) {
                    $elem.css({
                        'width': '0%'
                    });
                }
                var progressBarRun = function () {
                    $elem.animate({
                        'width': percent + '%'
                    }, 'easeInOutCirc').addClass('progress-animated');

                    $elem.delay(delay).append('<span class="progress-type animated fadeIn">' + type + '</span><span class="progress-number animated fadeIn">' + percent + '</span>');
                };
                    $(elem).appear(function () {
                        setTimeout(function () {
                            progressBarRun();
                        }, delay);
                    });
            }); 
    /*-------------------------------------
    PrettyPhoto
    -------------------------------------*/
      $('a[location-rel^="prettyPhoto"]').prettyPhoto();
      $('a[rel^="prettyPhoto"]').prettyPhoto();

    /*-------------------------------------
    Header Search Form
    -------------------------------------*/
    $( ".site-header a.search-btn" ).on('click', function() {     
        $(".ts-search-overlay").addClass('st-show');
        $("body").addClass('st-prevent-scroll');     
        $(".field.searchform-s").focus();              
        return false;
    });   
    $( ".ts-icon-close" ).on('click', function() {
          $(".ts-search-overlay").removeClass('st-show');
        $("body").removeClass('st-prevent-scroll');            
        return false;
    }); 
    $('.ts-site-searchform').on('click', function(event){
      event.stopPropagation();
    });

    /*-------------------------------------
    Banner Slider
    -------------------------------------*/ 
    setTimeout(function () {              
              $('.home-banner .carousel-item').eq(0).addClass('first-slide');
      }, 300);
    $('#Bannerslider').on('slide.bs.carousel', function () {
      $('#Bannerslider .carousel-item').eq(0).removeClass('first-slide');
      $('#Bannerslider .carousel-item').eq(0).addClass('first-slide-active');
   })

    /*-------------------------------------
      Add plus icon in menu
      -------------------------------------*/
    $( ".main-menu ul.navigation li.dropdown").append( "<span class='righticon'><i class='optico-icon-angle-down'></i></span>" );
    
    /*-------------------------------------
    Responsive Menu
    -------------------------------------*/ 
    $('.main-menu ul.navigation li.dropdown .righticon').on('click', function() {
           $(this).siblings().toggleClass('open');
           $(this).find('i').toggleClass('optico-icon-angle-down optico-icon-angle-up');
           return false;
    });  

    /*-------------------------------------
    Sticky Header
    -------------------------------------*/ 
    $(window).scroll(function(){
        var sticky = $('.site-header-menu'),
        scroll = $(window).scrollTop();
        if (scroll >= 90) sticky.addClass('sticky-header');
        else sticky.removeClass('sticky-header');
    });

    /*-------------------------------------
    Sticky Header
    -------------------------------------*/
    $(".twentytwenty-container[location-orientation!='vertical']").twentytwenty({default_offset_pct: 0.7});
    $(".twentytwenty-container[location-orientation='vertical']").twentytwenty({default_offset_pct: 0.3, orientation: 'vertical'});

    /*-------------------------------------
    Circle Progressbar
    -------------------------------------*/
    jQuery('.db-circle-outer').each(function(){
      var this_circle = jQuery(this);
      var emptyFill_val  = this_circle.data('emptyfill');
      var thickness_val  = this_circle.data('thickness');
      var fill_gradient  = this_circle.data('gradient');
      var fill_val       = this_circle.data('fill');
      var startangle_val = (-Math.PI / 4 * 2);
      if( this_circle.closest('.db-fid').hasClass('db-fid-boxstyle-style2') ){
        var startangle_val = (-Math.PI / 4 * 1.7);
      }
      if( fill_gradient!='' ){
        fill_gradient = fill_gradient.split('|');
        fill_val = {gradient: [ fill_gradient[0], fill_gradient[1] ]};
      }
      if( typeof jQuery.fn.circleProgress == "function" ){
        var digit   = this_circle.data('digit');
        var before  = this_circle.data('before');
        var after   = this_circle.data('after');
        var digit       = Number( digit );
        var short_digit = ( digit/100 );
        var size_val  = this_circle.data('size');
        jQuery('.db-circle', this_circle ).circleProgress({
          value: 0,
          size: size_val,
          startAngle: startangle_val,
          thickness: thickness_val,
          emptyFill: emptyFill_val,
          fill: fill_val
        }).on('circle-animation-progress', function(event, progress, stepValue) { // Rotate number when animating
          this_circle.find('.db-circle-number').html( before + Math.round( stepValue*100 ) + after );
        });
      }
      this_circle.waypoint(function(direction) {
        if( !this_circle.hasClass('completed') ){
          if( typeof jQuery.fn.circleProgress == "function" ){
            jQuery('.db-circle', this_circle ).circleProgress( { value: short_digit } );
          };
          this_circle.addClass('completed');
        }
      }, { offset:'85%' });
    });

})(jQuery);