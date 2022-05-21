#!/bin/python3
# X fix update to use lines rather than area wipe.
# X center the text for city
# - log to /tmp
# - make graphics draw onto canvas, then swap canvases
# X when update, make sure time update too
# X Add the weather icon to the display
# X pass weather icon into the graphics
# - display detail maps, temp, icons
# - make 5 day display
# - add inserting options into argv from $RGB
from samplebase import SampleBase
import time

from PIL import Image
from PIL import ImageDraw
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

class OpenWeather(SampleBase):
    def __init__(self, args, **kwargs):
        super(OpenWeather, self).__init__(*args, **kwargs)
        print("in __init__")
        self.LOCATION=None
        
    # there is a bitmap of icons, day followed by night 9 or so deep each 16x16 pixels

    def get_icons(self):
        """Use icon_name to get the position of the sprite and update
        the current icon.

        :param icon_name: The icon name returned by openweathermap

        Format is always 2 numbers followed by 'd' or 'n' as the 3rd character
        """
        #be FAST after wiping the display so it doesn't flicker
        self.icons_dict = {}
        icon_map = ("01", "02", "03", "04", "09", "10", "11", "13", "50")
        for i in range(9):
            for j in range(2):
                #self.matrix.SetImage(self.image, 0, 20-8) # overlay white area for title at 1st line
                icon1=self.icons.crop( (j*16,i*16, j*16+16,i*16+16) )
                c3='d'
                if j == 1:
                    c3='n'
                c12=icon_map[i]
                icon_name=c12+c3
                self.icons_dict[ icon_name ] = icon1

                #self.matrix.SetImage(icon1, 80+78+12 + 8, 28-8) # overlay white area for title at 1st line
                #time.sleep(4)

    def display_icon(self, icon, x, y ):
        self.matrix.SetImage(self.icons_dict[icon], x, y) # overlay white area for title at 1st line

    def run(self):
        print("in run OW")
        self.icons=Image.open("owd_icons.bmp").convert('RGB')
        # self.parser.add_argument("-r", "--led-rows", action="store", help="Display rows. 16 for 16x32, 32 for 32x32. Default: 32", default=32, type=int)
        # Configuration for the matrix
        #options = RGBMatrixOptions()
        #print("return from RGBMatrixOptions")
        #options.rows = 64
        #options.cols = 64
        #options.chain_length = 4
        #options.parallel = 1
        #options.hardware_mapping = 'adafruit-hat-pwm'  # If you have an Adafruit HAT: 'adafruit-hat'
        #options.pwm_bits=11
        ##options.pwm_lsb_nanoseconds=50
        #options.brightness=3
        ##options.scan_mode=
        ##options.multiplexing=
        ##options.row_address_type=
        #options.show_refresh_rate=1
        #options.inverse_colors=0
        ##options.led_rgb_sequence=
        ##options.pixel_mapper_config=
        ##options.pwm_dither_bits=
        #options.gpio_slowdown=2
        #options.daemon=1
        #options.drop_privileges=0
        #options.disable_hardware_pulsing = True # if sudo, skip this
        #print("Matrix in")
        #matrix = RGBMatrix(options = options)
        #print("Matrix out")
        self.get_icons()
        font = None
        self.paint(None)

    def paint(self,LOCATION=None):
        #print("in paint")
        canvas = self.matrix
        self.font1 = graphics.Font()
        #self.font1.LoadFont("../fonts/7x13.bdf")
        self.font1.LoadFont("./fonts/7x13.bdf")
        self.font = graphics.Font()
        self.font.LoadFont("./fonts/5x7.bdf")
        self.red = graphics.Color(255, 0, 0)

        # Create a large area named "self.image" which can be copied to a Canvas/matrix
        self.image = Image.new("RGB", (256, 64-20+8))  # A clean area to refresh a section of the display
        draw = ImageDraw.Draw(self.image)  # Declare Draw instance before prims. Use PIL to draw
        draw.rectangle((0, 0, 255, 49), fill=(4, 4, 0), outline=(192-40, 192-40, 0))

        #graphics.DrawLine(canvas, 5, 5, 22, 13, self.red)

        green = graphics.Color(0, 255, 0)
        #graphics.DrawCircle(canvas, 15, 15, 10, green)

        self.blue = graphics.Color(0, 0, 255)
        if LOCATION != None:
            self.matrix.Clear()
            outs=str(LOCATION)
        else:
            outs="YoNa Weather"
        graphics.DrawText(canvas, self.font1, 128 - len(outs)/2*7 , 10, self.blue, outs)

        #time.sleep(10)   # show display for 10 seconds before exit
        #print("out paint")

    def update_time(self,maybe_now=time.time()):
        #font = graphics.Font()
        #font.LoadFont("../fonts/5x7.bdf")
        #red = graphics.Color(255, 0, 0)
        rightnow=str( time.strftime('%-I:%M:%S %p', time.localtime(maybe_now)) )
        #timex=256-55
        timex=80+78+12 + 10
        #timey=20-7
        timey=44-7
        if False:
            image = Image.new("RGB", (89-35, 8)) 
            draw = ImageDraw.Draw(image)  # Declare Draw instance before prims
            draw.rectangle((0, 0, 89-35, 7), fill=(4, 4, 0))
            self.matrix.SetImage(image, timex, timey) # overlay white area
        else:
            background = graphics.Color(4, 4, 0)
            graphics.DrawLine(self.matrix, timex, timey+1, 256-2, timey+1, background)
            graphics.DrawLine(self.matrix, timex, timey+2, 256-2, timey+2, background)
            graphics.DrawLine(self.matrix, timex, timey+3, 256-2, timey+3, background)
            graphics.DrawLine(self.matrix, timex, timey+4, 256-2, timey+4, background)
            graphics.DrawLine(self.matrix, timex, timey+5, 256-2, timey+5, background)
            graphics.DrawLine(self.matrix, timex, timey+6, 256-2, timey+6, background)
        graphics.DrawText(self.matrix, self.font, timex, timey+7, self.red,rightnow)
 
    def update( self, location, lon, lat, id, main, description, icon, temp, feels_like, temp_min, temp_max, pressure, humidity, visibility, windspeed, winddeg, windgust, sunrise, sunset ):
        canvas = self.matrix

        #image = Image.new("RGB", (256, 64-20+8))  # Can be larger than matrix if wanted!!
        #draw = ImageDraw.Draw(self.image)  # Declare Draw instance before prims
        #draw.rectangle((0, 0, 255, 49), fill=(4, 4, 0), outline=(192-40, 192-40, 0))

        self.matrix.SetImage(self.image, 0, 20-8) # overlay white area
        #time.sleep(10)

        #font = graphics.Font()
        #font.LoadFont("../fonts/5x7.bdf")
        font=self.font

        ##be FAST after wiping the display so it doesn't flicker

        #background = graphics.Color(4, 4, 0)
        #for i in range(48):
        #    graphics.DrawLine(self.matrix, 2, 21-7+i, 256-2, 21-7+i, background)

        # just print out all the icons
        #icon_map = ("01", "02", "03", "04", "09", "10", "11", "13", "50")
        #for i in range(9):
        #    icon_name=icon_map[i]+"d"
        #    self.display_icon( icon_name, i*16, 20 )
        #    icon_name=icon_map[i]+"n"
        #    self.display_icon( icon_name, i*16, 20+20 )
        #    time.sleep(1)
        #time.sleep(40)

        #red = graphics.Color(255, 0, 0)
        red = self.red
        ax=2
        bx=80
        cx=80+78+12
        #graphics.DrawText(canvas, font, ax, 20, red,"  lon "+ str(lon))
        #graphics.DrawText(canvas, font, bx, 20, red,"  lat "+ str(lat)+" "+str(location))
        #graphics.DrawText(canvas, font, bx, 20, red," "+ str(location)[0:34])
        #graphics.DrawText(canvas, font, 128-len(str(location)[0:34])/2*5, 20, red,str(location)[0:34])
        #description+=" some more words and lots more words123456789"
        graphics.DrawText(canvas, font, 128-len(str(description)[0:50])/2*5, 20, red,str(description)[0:50])
        #graphics.DrawText(canvas, font, bx, 28, red, (str(description))[0:34])

        self.display_icon( icon, 80+78+12+8, 28-8 )

        graphics.DrawText(canvas, font, ax, 44, red," temp "+ str(temp) + " ºF")
        graphics.DrawText(canvas, font, ax, 52, red," like "+ str(feels_like) + " ºF")
        graphics.DrawText(canvas, font, ax, 60, red,"  min "+ str(temp_min) + " ºF")
        graphics.DrawText(canvas, font, ax, 36, red,"  max "+ str(temp_max) + " ºF")
        graphics.DrawText(canvas, font, bx, 36, red,"press "+ str(pressure) + " hPa")
        graphics.DrawText(canvas, font, ax, 28, red,"humid "+ str(humidity) + " %")
        graphics.DrawText(canvas, font, bx, 44, red,"  vis "+ str(visibility) + " ft")
        #graphics.DrawText(canvas, font, bx, 52, red," wind "+ str(windspeed) + " mph")
        if windgust != None:
            graphics.DrawText(canvas, font, bx, 52, red," wind "+ str(windspeed) + "+" + str(windgust) + " mph")
        else:
            graphics.DrawText(canvas, font, bx, 52, red," wind "+ str(windspeed) + " mph")
        graphics.DrawText(canvas, font, bx, 60, red,"  dir "+ str(winddeg) + " º")
        graphics.DrawText(canvas, font, cx, 52, red," rise "+ time.strftime('%-I:%M %p', time.localtime(sunrise)))
        graphics.DrawText(canvas, font, cx, 60, red,"  set "+ time.strftime('%-I:%M %p', time.localtime(sunset)))

# Main function
if __name__ == "__main__":
    OW=OpenWeather()
    if (not OW.process()):
        OpenWeather.print_help()
