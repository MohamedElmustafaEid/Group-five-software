var osm = new ol.layer.Tile({
	title: 'OpenStreetMap',
	type: 'base',
	visible: true,
	source: new ol.source.OSM()
});
var stamenWatercolor = new ol.layer.Tile({
title: 'Stamen Watercolor',
type: 'base',
visible: true,
source: new ol.source.Stamen({
layer: 'watercolor'
})
});
var stamenToner = new ol.layer.Tile({
title: 'Stamen Toner',
type: 'base',
visible: true,
source: new ol.source.Stamen({
layer: 'toner'
})
});

var bingRoads = new ol.layer.Tile({
title: 'Bing Maps—Roads',
type: 'base',
visible: true,
source: new ol.source.BingMaps({
key: 'AhVnxSFIxWx8p8gzW1oleRsLlHMN4NNXSSAqi2AEOBEP9tzBxWbQiDiZlOG4sdYR',
imagerySet: 'Road'
})
});

var bingAerial = new ol.layer.Tile({
title: 'Bing Maps—Aerial',
type: 'base',
visible: true,
source: new ol.source.BingMaps({
key: 'AhVnxSFIxWx8p8gzW1oleRsLlHMN4NNXSSAqi2AEOBEP9tzBxWbQiDiZlOG4sdYR',
imagerySet: 'Aerial'
})
});

var bingAerialWithLabels = new ol.layer.Tile({
title: 'Bing Maps—Aerial with Labels',
type: 'base',
visible: true,
source: new ol.source.BingMaps({
key: 'AhVnxSFIxWx8p8gzW1oleRsLlHMN4NNXSSAqi2AEOBEP9tzBxWbQiDiZlOG4sdYR',
imagerySet: 'AerialWithLabels'
})
});

var plosStandard = new ol.layer.Image({
	title: 'PLOS Standard Classes',
	type: 'Results',
	source: new ol.source.ImageWMS({
		url: 'http://localhost:8082/geoserver/wms',
		params: {'LAYERS': 'GIS_Lab:F.PLOS'}
	}),
	
});
var plosModified = new ol.layer.Image({
	title: 'PLOS Modified Classes',
	type: 'Results',
	source: new ol.source.ImageWMS({
		url: 'http://localhost:8082/geoserver/wms',
		params: {'LAYERS': 'GIS_Lab:F.PLOS.MOD'}
	}),
	
});
var enhancedPlosStandard = new ol.layer.Image({
	title: 'Enhanced PLOS Standard Classes',
	type: 'Results',
	source: new ol.source.ImageWMS({
		url: 'http://localhost:8082/geoserver/wms',
		params: {'LAYERS': 'GIS_Lab:E.PLOS'}
	}),
	
});
var enhancedPlosModified = new ol.layer.Image({
	title: 'Enhanced PLOS Modified Classes',
	type: 'Results',
	source: new ol.source.ImageWMS({
		url: 'http://localhost:8082/geoserver/wms',
		params: {'LAYERS': 'GIS_Lab:enhanced_plos'}
	}),
	
});

var map = new ol.Map({
	target: document.getElementById('map'),
	layers: [
	new ol.layer.Group({
		title: 'Base Maps',
		layers: [bingRoads,bingAerial,bingAerialWithLabels,stamenToner, stamenWatercolor,osm]
	}),
	new ol.layer.Group({
		title: 'Results',
		layers: [plosStandard,plosModified,enhancedPlosStandard,enhancedPlosModified]
	})
	],
	view: new ol.View({
		center: ol.proj.fromLonLat([9.164606,45.501319]),
		zoom: 16.8
	}),
	controls: ol.control.defaults().extend([
		new ol.control.ScaleLine(),
		new ol.control.FullScreen(),
		new ol.control.OverviewMap(),
		new ol.control.MousePosition({
			coordinateFormat: ol.coordinate.createStringXY(4),
			projection: 'EPSG:32632'
		})
		])
});
var layerSwitcher = new ol.control.LayerSwitcher({});
map.addControl(layerSwitcher);