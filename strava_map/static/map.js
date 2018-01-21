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
        $('#btn-fetchactivities').click(function () {
            self.fetchActivities();
        });
        $(document).on('click', '#activities .list-group-item', function () {
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
    },

    clearActivities: function() {
        $('#activities .list-group-item').remove();
    },

    fetchActivities: function() {
        $('#btn-fetchactivities').prop('disabled', true);
        this.clearActivities();
        $('#fetch-spinner').show();
        $.getJSON('/activities', function(data) {
            $('#fetch-spinner').hide();
            $.each(data, function(key, item) {
                var polyline = item['map']['summary_polyline'];
                if (!polyline) {
                    polyline = 'None';
                }
                $('#activities .list-group').append(
                    $('<div>')
                        .attr('class', 'list-group-item flex-column align-items-start')
                        .attr('data-id', item['id'])
                        .attr('data-polyline', polyline)
                        .append(
                            $('<h5>')
                                .attr('class', 'mb-1')
                                .append(item['name'])
                        )
                        .append(
                            $('<small>').append(item['type'])
                        )
                        .append(
                            $('<br />')
                        )
                        .append(
                            $('<small>').append('s=' + item['distance'])
                        )
                        .append(
                            $('<small>').append('t=' + item['elapsed_time'])
                        )
                        .append(
                            $('<br />')
                        )
                        .append(
                            $('<small>').append(item['start_date_local'])
                        )
                );
            });
            $('#btn-fetchactivities').prop('disabled', false);
        });
    }
};
