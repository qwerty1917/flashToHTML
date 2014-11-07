jQuery(document).ready(function($) {
 
        $(".navbar-brand").click(function(event){            
                event.preventDefault();
                $('html,body').animate({scrollTop:$(this.hash).offset().top}, 500);
        });//goto home button

        $(".navbar-about").click(function(event){            
                event.preventDefault();
                $('html,body').animate({scrollTop:$(this.hash).offset().top-90}, 500);
        });//goto row button

        $(".navbar-team").click(function(event){            
                event.preventDefault();
                $('html,body').animate({scrollTop:$(this.hash).offset().top-90}, 500);
        });//goto team button

        $(".btn.btn-default.first").click(function(event){            
                event.preventDefault();
                $('html,body').animate({scrollTop:$(this.hash).offset().top-20}, 500);
        });//goto reading button

        $(".btn.btn-default.second").click(function(event){            
                event.preventDefault();
                $('html,body').animate({scrollTop:$(this.hash).offset().top-20}, 500);
        });//goto assume button

        $(".btn.btn-default.third").click(function(event){
                event.preventDefault();
                $('html,body').animate({scrollTop:$(this.hash).offset().top-20}, 500);
        });//goto write button
});