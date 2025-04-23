import streamlit as st
from sqlalchemy import text

def data_conn():
    conn = st.connection('objects_db', type='sql')

    # Insert some data with conn.session.
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
            (14, 'Hercules', 'Messier 31', 'Cluster', +5.8, 'Globular Cluster. Telescope required to see its shape'),
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

    # Query and display the data you inserted
    objects_df = conn.query('select * from objects')
    return objects_df