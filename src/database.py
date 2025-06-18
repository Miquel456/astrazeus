import streamlit as st
from sqlalchemy import text

def data_conn():
    """
    Create the file objects.db for 15 stellar objects: 5 are stars, 5 are planets and 5 are cluster, galaxy or nebula.
    The language used is SQLAlchemy.
    The columns are: id, name, name_2, ob_type (object type), mag_aparent (aparent magnitude), description with
    primary key on id.
    The function returns the whole table.
    This function is used for querying to Astropy API, Simbad, to get object coordinates.
    """
    conn = st.connection('objects_db', type='sql')
    with conn.session as s:
        s.execute(text('DROP TABLE IF EXISTS objects;'))
        s.execute(text('CREATE TABLE IF NOT EXISTS objects ' \
                    '(id TEXT NOT NULL,' \
                    'name TEXT NOT NULL,' \
                    'name_2 TEXT NOT NULL,' \
                    'ob_type TEXT NOT NULL,' \
                    'mag_aparent NUMERIC NOT NULL,' \
                    'description TEXT,' \
                    'CONSTRAINT objects_pk PRIMARY KEY (id));'))
        data = [
            (1, 'Sirius', 'Alpha Canis Majoris', 'Star', -1.46, 'Canis Major constellation. Most brightness star in the night sky (North hemisphere)'),
            (2, 'Canopus', 'Alpha Carinae', 'Star', -0.74, 'Carine constellation. Second most brightness star in the night sky (South hemisphere)'),
            (3, 'Arcturus', 'Alpha Bootis', 'Star', -0.05, 'Bootes constellation. Orange Giant star'),
            (4, 'Vega', 'Alpha Lyrae', 'Star', +0.03, "Lyra constellation. Summer triangle's star"),
            (5, 'Capella', 'Alpha Aurigae', 'Star', +0.08, 'Auriga constellation. Visible on winter'),
            (6, 'Venus', 'None', 'Planet', -3.8, "Earth's twin. First brightness planetary object after Sun and Moon"),
            (7, 'Jupiter', 'None', 'Planet', -1.6, 'Biggest planet. Very bright'),
            (8, 'Saturn', 'None', 'Planet', +1.0, 'Planet with notorious rings. Less bright than others, but still visible'),
            (9, 'Mars', 'None', 'Planet', +1.8, 'Red planet. Visible every 2 years'),
            (10, 'Mercury', 'None', 'Planet', +5.5, 'Hottest planet. Visible during twilight'),
            (11, 'Pleiades', 'Messier 45', 'Cluster', +1.6, 'Open Cluster. Can be visible with the naked eye'),
            (12, 'Andromeda', 'Messier 31', 'Galaxy', +3.4, 'Spiral Galaxy. Visible with the naked eye during dark nights'),
            (13, 'Orion', 'Messier 42', 'Nebula', +4.0, 'Emission Nebula. Easy to track'),
            (14, 'Hercules', 'Messier 13', 'Cluster', +5.8, 'Globular Cluster. Telescope required to see its shape'),
            (15, 'Ring Nebula', 'Messier 57', 'Nebula', +8.8, 'Planetary Nebula. Telescope required')
        ]
        query = text("""
                        INSERT INTO objects (id, name, name_2, ob_type, mag_aparent, description)
                        VALUES (:id, :name, :name_2, :ob_type, :mag_aparent, :description)
                    """)
        for row in data:
            s.execute(query, {
                "id": row[0],
                "name": row[1],
                "name_2": row[2],
                "ob_type": row[3],
                "mag_aparent": row[4],
                "description": row[5]
            })
        s.commit()
    objects_df = conn.query('select * from objects')
    return objects_df

def astro_data_recommendation():
    """
    A list is created where in every index a dictionary is made to describe the astronomical object.
    There are 5 stars and 5 objects from galaxies, clusters and nebula.
    For each object, it is described the name, category, ra (right ascension), dec (declination),
    app_mag (apparent magnitude), abs_mag (absolute magnitude), mass, radius, distance (from Earth), 
    interest (activity user) and active (used for ML recommendation)
    This function returns the whole list.
    """
    data = []
    data.append({'name': 'Sirius', 
                 'category': 'Star', 
                 'ra': 6.752477022222222, 
                 'dec': -16.71611586111111, 
                 'app_mag': -1.46, 
                 'abs_mag': +1.43, 
                 'mass': 2.06, 
                 'radius': 1.257461921422305e-07, 
                 'distance': 8.6, 
                 'interest': 0, 
                 'active': False})
    data.append({'name': 'Canopus', 
                 'category': 'Star', 
                 'ra': 6.399197188888889, 
                 'dec': -52.69566138888889, 
                 'app_mag': -0.74, 
                 'abs_mag': -5.71, 
                 'mass': 9.4, 
                 'radius': 5.390173031593856e-06, 
                 'distance': 310, 
                 'interest': 0, 
                 'active': False})
    data.append({'name': 'Arcturus', 
                 'category': 'Star', 
                 'ra': 14.261020019444445, 
                 'dec': 19.18240916666667, 
                 'app_mag': -0.05, 
                 'abs_mag': -0.3, 
                 'mass': 1.08, 
                 'radius': 1.867808935913833e-06, 
                 'distance': 36.7, 
                 'interest': 0, 
                 'active': False})
    data.append({'name': 'Vega', 
                 'category': 'Star', 
                 'ra': 18.61564898611111, 
                 'dec': 38.78368894444444, 
                 'app_mag': +0.03, 
                 'abs_mag': +0.58, 
                 'mass': 2.15, 
                 'radius': 1.8531017789381335e-07, 
                 'distance': 25, 
                 'interest': 0, 
                 'active': False})
    data.append({'name': 'Capella', 
                 'category': 'Star', 
                 'ra': 5.2781551972222225, 
                 'dec': 45.997991472222225, 
                 'app_mag': +0.08, 
                 'abs_mag': 0.30, 
                 'mass': 2.5, 
                 'radius': 8.08893633663471e-07, 
                 'distance': 42.92, 
                 'interest': 0, 
                 'active': False})
    data.append({'name': 'Pleiades', 
                 'category': 'Cluster', 
                 'ra': 3.773388888888889, 
                 'dec': 24.11388888888889, 
                 'app_mag': +1.6, 
                 'abs_mag': -4.31, 
                 'mass': 800, 
                 'radius': 24.34, 
                 'distance': 440, 
                 'interest': 0, 
                 'active': False})
    data.append({'name': 'Orion', 
                 'category': 
                 'Nebula', 
                 'ra': 5.588, 
                 'dec': -5.3875, 
                 'app_mag': +4.0, 
                 'abs_mag': -4.1, 
                 'mass': 2000, 
                 'radius': 12, 
                 'distance': 1500, 
                 'interest': 0, 
                 'active': False})
    data.append({'name': 'Hercules', 
                 'category': 'Cluster', 
                 'ra': 16.694898333333335, 
                 'dec': 36.46131944444445, 
                 'app_mag': +8.5, 
                 'abs_mag': -8.55, 
                 'mass': 700000, 
                 'radius': 72.5, 
                 'distance': 25000, 
                 'interest': 0, 
                 'active': False})
    data.append({'name': 'Ring Nebula', 
                 'category': 'Nebula', 
                 'ra': 18.893082434975334, 
                 'dec': 33.029134246539996, 
                 'app_mag': +15.769, 
                 'abs_mag': -0.3, 
                 'mass': 1.2, 
                 'radius': 1.3, 
                 'distance': 2500, 
                 'interest': 0, 
                 'active': False})
    data.append({'name': 'Andromeda', 
                 'category': 'Galaxy', 
                 'ra': 0.7123138888888888, 
                 'dec': 41.26875, 
                 'app_mag': +3.44, 
                 'abs_mag': -21.5, 
                 'mass': 800000000000, 
                 'radius': 110000, 
                 'distance': 2537000, 
                 'interest': 0, 
                 'active': False})
    return data

def astro_object_description(name):
    """
    This function recives input 'name', according to 'objects.db', to return a descriptive text and image, if possible,
    from the object selected via input.
    There are descriptions for all objects in 'objects.db'.
    'params' object is a dictionary used to generate the text description using model 'gpt-3.5-turbo'.
    'url' object is the path where image is extracted.
    """
    if name == "Andromeda":
        text = '''Andromeda, also known as the Andromeda Galaxy, is a massive spiral galaxy located a 
        staggering 2.5 million light-years away from Earth. 🌌✨

        This galactic giant boasts a remarkable mass equivalent to a whopping 800 billion times that of our Sun, 
        and it spans an immense radius of 110,000 light-years. To put this into perspective, Andromeda is about the same size
        as our Milky Way galaxy, making it one of the largest cosmic structures in our cosmic neighborhood. 🌠🔭

        Despite its immense distance, Andromeda shines brightly in our night sky with an apparent magnitude of +3.44, 
        making it visible to the naked eye under dark skies. However, its absolute magnitude of -21.5 reveals that Andromeda is 
        even more luminous than it appears from Earth, outshining many individual stars within its vast expanse. 🌟💫

        Studying Andromeda not only offers us a glimpse into the mysteries of our universe but also ignites our imagination about 
        the countless wonders waiting to be discovered beyond our own cosmic backyard. 🧑‍🚀🖖
        '''
        params = {
                'name': 'Andromeda',
                'category': 'Galaxy',
                'ra': '00 42 44.330',
                'dec': '+41 16 07.50',
                'app_mag': '+3.44',
                'abs_mag': '-21.5',
                'mass': '800000000000 solar masses',
                'radius': '110000 light-years',
                'distance': '2537000 ligh-years'
            }
        image = "images/library/andromeda_hubble.webp"
        url = "https://esahubble.org/images/heic2501a/"
    if name == "Ring Nebula":
        text = '''Behold the Ring Nebula, a stunning planetary nebula located approximately 2500 light-years away from Earth 
        in the constellation of Lyra! This celestial beauty, with a captivating name that suits its appearance, is a glowing 
        remnant of a dying star's final stages.

        With a mass of 1.2 times that of our Sun and a radius stretching 1.3 light-years across, the Ring Nebula showcases the 
        grandeur and complexity of the universe. Despite its immense size, the Ring Nebula's absolute magnitude of -0.3 reveals 
        its faintness when viewed from afar, with an apparent magnitude of +15.769.

        As we gaze upon this cosmic spectacle, we are reminded of the vastness of space and the intricate processes that shape 
        the cosmos. The Ring Nebula serves as a mesmerizing example of the beauty that emerges from the cycle of stellar life 
        and death, leaving us in awe of the wonders that lie beyond our world. 🧑‍🚀🖖
        '''
        params = {
            'name': 'Ring Nebula',
            'category': 'Planetary Nebula',
            'ra': '18 53 35.0967659112',
            'dec': '+33 01 44.883287544',
            'app_mag': '+15.769',
            'abs_mag': '-0.3',
            'mass': '1.2 solar masses',
            'radius': '1.3 light-years',
            'distance': '2500 light-years'
        }
        image = "images/library/ring_nebula_hubble.webp"
        url = "https://esahubble.org/images/heic1310a/"
    if name == "Hercules":
        text = '''In the vast expanse of our galaxy, there exists a stunning celestial jewel known as Hercules. 
        But Hercules isn't your average star or planet - it belongs to a special category called a Globular Cluster. 
        Imagine a tightly-knit community of stars, all bound together by gravity, creating a mesmerizing cosmic 
        dance in the depths of space.

        Located a whopping 25,000 light-years away from our own planet Earth, Hercules boasts an apparent magnitude of 
        +8.5, making it visible through a good pair of binoculars on a dark, clear night. Despite its seeming brightness, 
        its absolute magnitude of -8.55 reveals its true luminosity when compared to other celestial objects.

        With a mass equivalent to a staggering 700,000 times that of our Sun and a radius spanning 72.5 light-years, 
        Hercules stands as a testament to the sheer scale and grandeur of the cosmos. Just picture a colossal spherical 
        gathering of stars, each one playing its part in the symphony of the universe.

        So next time you gaze up at the night sky, remember the distant beauty of Hercules, a celestial marvel that reminds us 
        of the boundless wonders waiting to be explored beyond our own cosmic neighborhood. 🧑‍🚀🖖
        '''
        params = {
            'name': 'Hercules',
            'category': 'Globular Cluster',
            'ra': '16 41 41.634',
            'dec': '+36 27 40.75',
            'app_mag': '+8.5',
            'abs_mag': '-8.55',
            'mass': '700000 solar masses',
            'radius': '72.5 light-years',
            'distance': '25000 light-years'
        }
        image = "images/library/hercules_hubble.webp"
        url = "https://esahubble.org/images/potw1011a/"
    if name == "Orion":
        text = '''Welcome to the mesmerizing world of astronomy, where we will embark on a journey to explore the breathtaking 
        Orion Nebula! ✨🪐

        Located approximately 1500 light-years away from Earth, the Orion Nebula is a stunning celestial cloud of gas and dust 
        where new stars are being born. With a mass equivalent to 2000 times that of our Sun, this cosmic beauty spans an 
        impressive radius of 12 light-years, making it a true giant in the vastness of space.

        Shining in the night sky with an apparent magnitude of +4.0, the Orion Nebula dazzles observers with its radiant glow. 
        But don't let its brightness fool you, for its absolute magnitude of -4.1 reveals the true luminosity of this stellar 
        nursery, outshining many other objects in the night sky.

        As we gaze upon this celestial masterpiece, let us marvel at the wonders of the universe and the sheer magnitude of creation 
        unfolding before our eyes. The Orion Nebula serves as a reminder of the beauty and complexity of the cosmos, 
        igniting a sense of wonder and curiosity within us all. 🧑‍🚀🖖
        '''
        params = {
            'name': 'Orion',
            'category': 'Nebula',
            'ra': '05 35 16.8',
            'dec': '-05 23 15',
            'app_mag': '+4.0',
            'abs_mag': '-4.1',
            'mass': '2000 solar masses',
            'radius': '12 light-years',
            'distance': '1500 light-years'
        }
        image = "images/library/orion_hubble.webp"
        url = "https://esahubble.org/images/heic0601a/"
    if name == "Pleiades":
        text = '''In the vast cosmic ocean, there exists a mesmerizing group of stars known as the Pleiades, or the Seven Sisters. 
        This celestial wonder is not just any ordinary star cluster; it's an open star cluster, a sparkling community of stars 
        bound together by gravity ✨.

        Located about 440 light-years away from Earth, the Pleiades cluster dazzles us with its beauty, shining with an 
        apparent magnitude of +1.6, making it visible to the naked eye in the night sky 🌌. While we can see its shimmer from afar, 
        the absolute magnitude of the Pleiades remains undefined, adding a mysterious allure to these distant stars.

        Comprising around 800 times the mass of our own Sun, the Pleiades cluster is like a cosmic family, with each star playing 
        its unique role in the dance of the universe. Stretching out over 24.34 light-years, the cluster's expanse is a 
        sight to behold, captivating astronomers and stargazers alike.

        So, next time you gaze up at the night sky and spot the Pleiades, remember that you're witnessing a celestial masterpiece, 
        a stellar spectacle that has inspired wonder and curiosity for centuries 🧑‍🚀🖖.
        '''
        params = {
            'name': 'Pleiades',
            'category': 'Open Star Cluster',
            'ra': '03 46 24.2',
            'dec': '+24 06 50',
            'app_mag': '+1.6',
            'abs_mag': 'Undefined',
            'mass': '800 solar masses',
            'radius': '24.34 light-years',
            'distance': '440 light-years'
        }
        image = ""
    if name == "Capella":
        text = '''Meet Alpha Aurigae, also known as Capella, a dazzling star located approximately 42.92 light-years away from 
        Earth in the constellation of Auriga. 🌟✨

        This celestial beauty boasts a mass of 2.5 times that of our Sun and a radius a whopping 11 times larger! 
        Imagine a star so massive and grand, shining brightly in the night sky. 🌌💫

        With an apparent magnitude of +0.08, Alpha Aurigae outshines many other stars we see from Earth. But here's the fascinating part: 
        its absolute magnitude is just 0.30, which means if this star were placed at a standard distance, it would appear 
        even brighter to us!

        Next time you gaze up at the stars, remember Alpha Aurigae, a true giant in the vast cosmic ocean, 
        beckoning us to explore and marvel at the wonders of the universe. 🧑‍🚀🖖
        '''
        params = {
            'name': 'Alpha Aurigae or Capella',
            'category': 'Star',
            'ra': '05 16 41.35871',
            'dec': '+45 59 52.7693',
            'app_mag': '+0.08',
            'abs_mag': '0.30',
            'mass': '2.5 solar masses',
            'radius': '11 solar radius',
            'distance': '42.92 light-years'
        }
        image = ""
    if name == "Vega":
        text = '''In the vast expanse of our night sky shines Alpha Lyrae, also known as Vega, a dazzling star located 
        around 25 light-years away from Earth. 🌟 With an apparent magnitude of +0.03, Vega sparkles brightly in the 
        constellation of Lyra. Its absolute magnitude of +0.58 reveals that Vega is actually more luminous than our own Sun. ☀️

        Weighing in at 2.15 times the mass of the Sun and stretching to a radius 2.52 times larger, 
        Vega is a stellar powerhouse in our cosmic neighborhood. Its coordinates in the sky place it at 
        Right Ascension 18 hours 36 minutes and 56.33635 seconds, with a Declination of +38 degrees 47 minutes and 01.2802 seconds.

        Staring up at the night sky, it's awe-inspiring to think about the sheer size and brilliance of stars like Vega, 
        reminding us of the vast wonders that exist beyond our own planet. Let Vega's light guide your imagination 
        to explore the mysteries of the universe! 🧑‍🚀🖖
        '''
        params = {
            'name': 'Alpha Lyrae or Vega',
            'category': 'Star',
            'ra': '18 36 56.33635',
            'dec': '+38 47 01.2802',
            'app_mag': '+0.03',
            'abs_mag': '+0.58',
            'mass': '2.15 solar masses',
            'radius': '2.52 solar radius',
            'distance': '25 light-years'
        }
        image = ""
    if name == "Arcturus":
        text = '''Meet Alpha Bootis, also known as Arcturus, a dazzling star located approximately 36.7 light-years 
        away from Earth in the constellation of Bootes. 🌟

        This celestial giant boasts a mass of 1.08 times that of our Sun and a whopping radius of 25.4 times that of the Sun, 
        making it a true stellar behemoth. Despite its impressive size, Arcturus appears slightly dimmer in our 
        night sky with an apparent magnitude of -0.05, compared to the Sun's radiant -26.74. 
        However, don't let its brightness fool you, as its absolute magnitude of -0.3 reveals its intrinsic luminosity.

        Glowing with a warm orange hue, Arcturus stands out in the night sky as one of the brightest stars visible to 
        the naked eye. Its light has traveled through space for over three decades to reach us here on Earth, 
        offering a glimpse into the vastness and beauty of our universe. ✨🪐🖖
        '''
        params = {
            'name': 'Alpha Bootis or Arcturus',
            'category': 'Star',
            'ra': '14 15 39.67207',
            'dec': '+19 10 56.6730',
            'app_mag': '-0.05',
            'abs_mag': '-0.3',
            'mass': '1.08 solar masses',
            'radius': '25.4 solar radius',
            'distance': '36.7 light-years'
        }
        image = ""
    if name == "Canopus":
        text = '''In the vast cosmic ocean, there shines a brilliant star named Alpha Carinae, also known as Canopus. 
        This celestial beauty dazzles in the night sky with an apparent magnitude of -0.74, making it one of the brightest 
        stars visible from Earth. Despite its luminous appearance, Canopus actually hails from a distant realm, 
        residing 310 light-years away from our planet.

        Weighing in at a hefty 9.4 times the mass of our Sun and boasting a radius a whopping 73.3 times larger, 
        Canopus truly commands a stellar presence in the cosmos. To put this into perspective, imagine a star so massive 
        that it could engulf our entire solar system with ease!

        But what about its luminosity compared to our Sun? Well, while Canopus may seem bright to us, 
        its absolute magnitude of -5.71 pales in comparison to the Sun's 4.83. This goes to show the sheer diversity and 
        grandeur of the stars that populate our universe.

        So, the next time you gaze up at the night sky and spot Canopus twinkling in the southern heavens, remember the 
        immense scale and beauty of this distant stellar giant. Let its radiance inspire you to dream of the wonders that lie 
        beyond our world 🧑‍🚀🖖.
        '''
        params = {
            'name': 'Alpha Carinae or Canopus',
            'category': 'Star',
            'ra': '06 23 57.10988',
            'dec': '-52 41 44.3810',
            'app_mag': '-0.74',
            'abs_mag': '-5.71',
            'mass': '9.4 solar masses',
            'radius': '73.3 solar radius',
            'distance': '310 light-years'
        }
        image = ""
    if name == "Sirius":
        text = '''In the vast cosmic ocean, there shines a brilliant star known as Alpha Canis Majoris or Sirius. 
        Located a mere 8.6 light-years away from our own little blue planet, Sirius graces the night sky with its mesmerizing glow. 🌟

        This celestial gem boasts a mass of 2.06 times that of our Sun and a radius 1.71 times larger, making it a stellar 
        heavyweight in its own right. Despite its impressive size, Sirius appears incredibly bright to us Earthlings, with an 
        apparent magnitude of -1.46. To put this into perspective, our Sun, while vital for life as we know it, has a much 
        dimmer apparent magnitude of -26.74.

        What truly sets Sirius apart is its absolute magnitude of +1.43, revealing its intrinsic luminosity if 
        observed from a standard distance. This star dazzles us not only with its brilliance but also with its 
        unique characteristics that continue to captivate astronomers and stargazers alike. 🪐🖖
        '''
        params = {
            'name': 'Alpha Canis Majoris or Sirius',
            'category': 'Star',
            'ra': '06 45 08.91728',
            'dec': '-16 42 58.0171',
            'app_mag': '-1.46',
            'abs_mag': '+1.43',
            'mass': '2.06 solar masses',
            'radius': '1.71 solar radius',
            'distance': '8.6 light-years'
        }
        image = "images/library/sirius_a_b_hubble.webp"
        url = "https://esahubble.org/images/heic0516a/"
    if name == 'Venus':
        text = '''Venus, the dazzling planet in our night sky, is a beauty to behold! With an apparent magnitude ranging 
        between -4.92 to -2.98, it shines brightly, catching the eye of stargazers worldwide. Despite its allure, 
        Venus hides a mystery beneath its surface. 🌌

        This planet, with a mass of 0.82 times that of Earth 🌍, and a radius 0.95 times that of our home planet, 
        intrigues astronomers and space enthusiasts alike. Located at a variable distance from Earth, Venus never 
        fails to captivate us with its celestial dance. ✨

        Comparing Venus to Earth, we see the wonders of our universe unfold. Imagine a world with similar characteristics 
        to ours but with its own unique charm. Studying Venus not only expands our understanding of planetary science 
        but also fuels our curiosity about the vast cosmos beyond. 🧑‍🚀🖖
        '''
        params = {
            'name': 'Venus',
            'category': 'Planet',
            'ra': 'variable',
            'dec': 'variable',
            'app_mag': 'between -4.92 to -2.98',
            'abs_mag': '-4.4',
            'mass': '0.82 earth masses',
            'radius': '0.95 earth radius',
            'distance': 'variable'
        }
        image = "images/library/venus_hubble.webp"
        url = "https://esahubble.org/images/opo9516g/"
    if name == 'Jupiter':
        text = '''Imagine a colossal gas giant, named Jupiter, hanging gracefully in the vastness of space. With its 
        stunning beauty and immense size, Jupiter is a true marvel of our solar system. 🪐

        Jupiter, often called the "King of the Planets," boasts an apparent magnitude that varies between -2.94 to -1.66, 
        making it one of the brightest objects in our night sky. Its absolute magnitude, a measure of its brightness 
        as seen from a standard distance, is an impressive -9.4.

        This behemoth planet is a heavyweight champion, tipping the scales at a whopping 317.8 times the mass of our home planet, 
        Earth. To put this into perspective, Jupiter's radius is about 11.2 times that of Earth, 
        showcasing its vast size and dominating presence.

        Despite its distance from Earth constantly changing, Jupiter never fails to captivate us with its 
        sheer grandeur and beauty as it dances through the cosmos. Studying Jupiter not only unlocks the mysteries 
        of our solar system but also fuels our curiosity about the wonders of the universe. 🧑‍🚀🖖
        '''
        params = {
            'name': 'Jupiter',
            'category': 'Planet',
            'ra': 'variable',
            'dec': 'variable',
            'app_mag': 'between -2.94 to -1.66',
            'abs_mag': '-9.4',
            'mass': '317.8 earth masses',
            'radius': '11.2 earth radius',
            'distance': 'variable'
        }
        image = "images/library/jupiter_hubble.webp"
        url = "https://esahubble.org/images/heic1410a/"
    if name == 'Saturn':
        text = '''Saturn, the magnificent planet known for its stunning rings, is a true marvel in our solar system. 
        With a majestic appearance in the night sky, Saturn shines with an apparent magnitude ranging from -0.55 to +1.17, 
        making it easily visible to the naked eye. Despite its beauty, Saturn holds a mighty mass of 95.16 Earth masses, 
        dwarfing our own planet in comparison. 🌌

        The ringed giant boasts a radius of 9.14 times that of Earth, emphasizing its colossal size and grandeur. 
        As Saturn dances through space at a variable distance from Earth, its presence captivates astronomers and stargazers 
        alike with its celestial charm. 🪐🧑‍🚀🖖
        '''
        params = {
            'name': 'Saturn',
            'category': 'Planet',
            'ra': 'variable',
            'dec': 'variable',
            'app_mag': 'between -0.55 to +1.17',
            'abs_mag': '-9.7',
            'mass': '95.16 earth masses',
            'radius': '9.14 earth radius',
            'distance': 'variable'
        }
        image = "images/library/saturn_hubble.webp"
        url = "https://esahubble.org/images/heic1814b/"
    if name == 'Mars':
        text = '''Mars, the red planet, is a captivating member of our solar system. From our vantage point on Earth, 
        Mars can appear as bright as a star in the night sky, with its apparent magnitude ranging from -2.94 to +1.86. 
        Despite its varying distance from us, it always manages to catch our eye with its rusty glow.

        Compared to Earth, Mars is a bit of a lightweight, with only 0.11 times the mass of our home planet. 
        Its radius is also smaller, measuring at 0.53 times that of Earth. These differences give Mars its own unique
        character and set it apart in our cosmic neighborhood.

        Imagine standing on the surface of Mars, gazing up at the vast expanse of space. What a thrilling experience it would be! 
        Studying Mars not only teaches us about the planet itself but also provides valuable insights into the formation and 
        evolution of rocky worlds like our own.

        Next time you look up at the night sky and spot Mars shining brightly, remember the wonders that await us 
        in the universe. Exploration, discovery, and the mysteries of space are all out there, just waiting for us to reach 
        out and touch the stars. 🧑‍🚀🖖
        '''
        params = {
            'name': 'Mars',
            'category': 'Planet',
            'ra': 'variable',
            'dec': 'variable',
            'app_mag': 'between -2.94 to +1.86',
            'abs_mag': '-1.5',
            'mass': '0.11 earth masses',
            'radius': '0.53 earth radius',
            'distance': 'variable'
        }
        image = "images/library/mars_hubble.webp"
        url = "https://esahubble.org/images/opo0124a/"
    if name == 'Mercury':
        text = '''Mercury, the swift messenger of the gods in Roman mythology, is the smallest and innermost planet 
        in our solar system. Despite its petite size, this tiny world packs a punch! 🌌

        With an apparent magnitude that can range from -2.48 to +7.25, Mercury can be a challenging sight in the sky, 
        but its absolute magnitude of -0.4 reveals its true brightness. 💫

        Compared to Earth, Mercury is a lightweight, tipping the scales at just 0.06 times the mass of our home planet. 
        Its radius, measuring only 0.38 times that of Earth, showcases its compact nature. 🌏

        Mercury dances around the Sun at a variable distance, always staying relatively close to our star. 
        Its movements in the sky have captivated astronomers for centuries, offering a glimpse into the complexities 
        of our solar system. 🪐🧑‍🚀🖖
        '''
        params = {
            'name': 'Mercury',
            'category': 'Planet',
            'ra': 'variable',
            'dec': 'variable',
            'app_mag': 'between -2.48 to +7.25',
            'abs_mag': '-0.4',
            'mass': '0.06 earth masses',
            'radius': '0.38 earth radius',
            'distance': 'variable'
        }
        image = ""
    return text, image