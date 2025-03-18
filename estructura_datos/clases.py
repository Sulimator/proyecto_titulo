# Clase genérica para estampillas
class Stamp:
    def __init__(self, oid, candid, ra, dec):
        self.oid = oid
        self.candid = candid
        self.ra = ra
        self.dec = dec


# Clase específica de estampillas ZTF
class Stamp_ZTF(Stamp):
    def __init__(self, oid, candid, ra, dec, science_image, ref_image, diff_image):
        super().__init__(oid, candid, ra, dec)
        self.science_image = science_image
        self.ref_image = ref_image
        self.diff_image = diff_image


# Clase genérica de imágenes multiresolución
class MRimg:
    def __init__(self, multires_images=None):
        self.multires_images = multires_images if multires_images else {}


# Clase específica de imágenes multiresolucion de PS1
class PS1_MRimg(MRimg):
    def __init__(self, multires_images):
        super().__init__(multires_images)


# Clase MMObject que combina Stamp_ZTF y PS1_MRimg
class MMObject(Stamp_ZTF, PS1_MRimg):
    def __init__(self, oid, candid, ra, dec, science_image, ref_image, diff_image, class_label, multires_images=None):
        # Inicializar Stamp_ZTF
        Stamp_ZTF.__init__(self, oid, candid, ra, dec, science_image, ref_image, diff_image)
        # Inicializar PS1_MRimg
        PS1_MRimg.__init__(self, multires_images)
        self.class_label = class_label

# Clase contenedora de múltiples MMObject
class MMobjects:
    def __init__(self, objs=None):
        """
        Contenedor de múltiples objetos MMObject.
        
        :param objs: Lista opcional de objetos MMObject.
        """
        self.objs = objs if objs else []

    def add_object(self, mm_object):
        """Agrega un objeto MMObject a la lista."""
        if isinstance(mm_object, MMObject):
            self.objs.append(mm_object)
        else:
            raise TypeError("El objeto debe ser una instancia de MMObject")

    def show_all(self):
        """Muestra información de todos los MMObject almacenados."""
        print(f"Total de objetos: {len(self.objs)}")
        for i, obj in enumerate(self.objs, 1):
            print(f"\nObjeto {i}:")
            obj.show_info()

