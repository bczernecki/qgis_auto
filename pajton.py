#coding=utf-8
import sys
from qgis.core import (
    QgsProject, QgsComposition, QgsApplication, QgsProviderRegistry)
from qgis.gui import QgsMapCanvas, QgsLayerTreeMapCanvasBridge
from PyQt4.QtCore import *
from PyQt4.QtXml import QDomDocument
from PyQt4.QtGui import QImage
from PyQt4.QtGui import QPainter


gui_flag = True
app = QgsApplication(sys.argv, gui_flag)

# Make sure QGIS_PREFIX_PATH is set in your env if needed!
app.initQgis()

# Probably you want to tweak this
project_path = '/home/bartosz/github/qgis_auto/projekt.qgs'
# and this
template_path = '/home/bartosz/github/szablon_composer.qpt'

# Set output DPI
dpi = 200

canvas = QgsMapCanvas()
# Load our project
QgsProject.instance().read(QFileInfo(project_path))
bridge = QgsLayerTreeMapCanvasBridge(
    QgsProject.instance().layerTreeRoot(), canvas)
bridge.setCanvasLayers()

template_file = file(template_path)
template_content = template_file.read()
template_file.close()
document = QDomDocument()
document.setContent(template_content)
ms = canvas.mapSettings()
composition = QgsComposition(ms)
composition.loadFromTemplate(document, {})
# You must set the id in the template
#map_item = composition.getComposerItemById('map')
map_item = composition.getComposerMapById(1)
#map_item.setMapCanvas(canvas)
#map_item.zoomToExtent(canvas.extent())
# You must set the id in the template
#legend_item = composition.getComposerItemById('legend')
#legend_item.updateLegend()
composition.refreshItems()

dpmm = dpi / 25.4
#width = int(dpmm * composition.paperWidth())
width = int(1400)
print(width)

#height = int(dpmm * 141)
height = int(1000)
print(height)

# create output image and initialize it
image = QImage(QSize(width, height), QImage.Format_ARGB32)
#image.setDotsPerMeterX(dpmm * 1000)
#image.setDotsPerMeterY(dpmm * 1000)
#image.fill(0)

# set image's background color
#color = QColor(255, 255, 255)
# render the composition
imagePainter = QPainter(image)
composition.renderPage(imagePainter, 0)
imagePainter.end()

image.save("obraz_wyjsciowy.png", "png")

QgsProject.instance().clear()
QgsApplication.exitQgis()
