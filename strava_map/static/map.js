$(function() {
    App.init();
});

var App = {
    init: function() {
        this.map = this.initMap();
        this.track = null;
        this.initEventHandlers();
    },
    
    initMap: function() {
        var map = L.map('map').setView([51.505, -0.09], 13);

        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);
        
        return map;
    },
    
    initEventHandlers: function() {
        var self = this;
        $('#activities .list-group-item').click(function () {
            $('#activities .list-group-item').removeClass('active');
            if (self.track) {
                self.track.remove();
                self.track = null;
            }
            
            $(this).addClass('active');
            data_polyline = $(this).data('polyline');
            if (data_polyline != 'None') {
                polyline = L.PolylineUtil.decode(data_polyline);
                self.track = L.polyline(polyline).addTo(self.map);
                self.map.fitBounds(self.track.getBounds());
            }
        });
    }
};
