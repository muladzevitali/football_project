function initMap() {
    var office = {lat: 52.4898177, lng: 13.3484436};
    var myIcon = {
        url: "../static/images/mapicon.svg", // url
        scaledSize: new google.maps.Size(27, 50), // scaled size
        origin: new google.maps.Point(0,0), // origin
        anchor: new google.maps.Point(50, 50) // anchor
    };
    var map = new google.maps.Map(
        document.getElementById('map'), {zoom: 16, center: office,
        
        styles: [
{
"elementType": "geometry",
"stylers": [
{
"visibility": "on"
}
]
},
{
"elementType": "labels.icon",
"stylers": [
{
"visibility": "off"
}
]
},
{
"elementType": "labels.text.fill",
"stylers": [
{
"color": "#616161"
}
]
},
{
"elementType": "labels.text.stroke",
"stylers": [
{
"color": "#f5f5f5"
}
]
},
{
"featureType": "administrative.land_parcel",
"elementType": "labels.text.fill",
"stylers": [
{
"color": "#bdbdbd"
}
]
},
{
"featureType": "landscape",
"stylers": [
{
"visibility": "on"
}
]
},
{
"featureType": "landscape",
"elementType": "geometry",
"stylers": [
{
"color": "#8b8282"
}
]
},
{
"featureType": "landscape",
"elementType": "labels",
"stylers": [
{
"visibility": "off"
}
]
},
{
"featureType": "poi",
"elementType": "geometry",
"stylers": [
{
"color": "#eeeeee"
}
]
},
{
"featureType": "poi",
"elementType": "labels.text.fill",
"stylers": [
{
"color": "#757575"
}
]
},
{
"featureType": "poi.park",
"elementType": "geometry",
"stylers": [
{
"color": "#e5e5e5"
}
]
},
{
"featureType": "poi.park",
"elementType": "labels.text.fill",
"stylers": [
{
"color": "#9e9e9e"
}
]
},
{
"featureType": "road",
"stylers": [
{
"visibility": "on"
}
]
},
{
"featureType": "road",
"elementType": "geometry",
"stylers": [
{
"color": "#a39f9f"
}
]
},
{
"featureType": "road",
"elementType": "labels",
"stylers": [
{
"visibility": "on"
}
]
},
{
"featureType": "road.arterial",
"elementType": "labels",
"stylers": [
{
"visibility": "off"
}
]
},
{
"featureType": "road.arterial",
"elementType": "labels.text.fill",
"stylers": [
{
"color": "#757575"
}
]
},
{
"featureType": "road.highway",
"elementType": "labels",
"stylers": [
{
"visibility": "on"
}
]
},
{
"featureType": "road.highway",
"elementType": "labels.text.fill",
"stylers": [
{
"color": "#616161"
}
]
},
{
"featureType": "road.local",
"elementType": "labels.text.fill",
"stylers": [
{
"color": "#9e9e9e"
}
]
},
{
"featureType": "transit",
"stylers": [
{
"visibility": "on"
}
]
},
{
"featureType": "transit.station",
"elementType": "geometry",
"stylers": [
{
"color": "#eeeeee"
}
]
},
{
"featureType": "water",
"elementType": "geometry",
"stylers": [
{
"color": "#c9c9c9"
}
]
},
{
"featureType": "water",
"elementType": "labels.text.fill",
"stylers": [
{
"color": "#9e9e9e"
}
]
}
]});
    var marker = new google.maps.Marker({position: office, map: map, icon: myIcon});
}

(function ($) {
    "use strict";


    /*==================================================================
    [ Focus Contact2 ]*/
    $('.input100').each(function(){
        $(this).on('blur', function(){
            if($(this).val().trim() != "") {
                $(this).addClass('has-val');
            }
            else {
                $(this).removeClass('has-val');
            }
        })    
    })
  
  
    /*==================================================================
    [ Validate ]*/
    var name = $('.validate-input input[name="name"]');
    var email = $('.validate-input input[name="email"]');
    var phone = $('.validate-input input[name="phone"]');
    var subject = $('.validate-input input[name="subject"]');
    var message = $('.validate-input textarea[name="message"]');


    $('.validate-form').on('submit',function(){
        var check = true;

        if($(name).val().trim() == ''){
            showValidate(name);
            check=false;
        }


        if($(email).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
            showValidate(email);
            check=false;
        }

        if($(phone).val().trim().match(/^[5][0-9]{8}$/) == null){
            showValidate(phone);
            check=false;
        }

        if($(subject).val().trim() == ''){
            showValidate(subject);
            check=false;
        }

        if($(message).val().trim() == ''){
            showValidate(message);
            check=false;
        }

        return check;
    });


    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
           $(".alert").addClass("d-none");
       });
    });

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }
    
    

})(jQuery);