# constant class
class Constant:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 100/AU # 1 AU = 100 px
    record_scale = 100/AU
    SUN_MASS = 1.988892e30

    def update_scale(self, zoom_scale):
        self.SCALE = self.record_scale*zoom_scale


k = Constant()
print(k.SCALE)
k.update_scale(k.AU)
print(k.SCALE)