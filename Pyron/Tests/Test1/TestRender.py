import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

Vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (0, 0, 1)
)

Edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (1, 2),
    (1, 4),
    (2, 3),
    (2, 4),
    (3, 4)
)

def Draw (_Vertices, _Edges):
    glLineWidth (5)
    glBegin (GL_LINES)

    for Edge in _Edges:
        for Vertex in Edge:
            glVertex3fv (_Vertices[Vertex])
            glColor3f (0, 1, 0)

    glEnd ()

def Run ():
    pygame.init ()
    Display = (800, 800)
    pygame.display.set_mode (Display, DOUBLEBUF|OPENGL)

    gluPerspective (45, (Display[0] / Display[1]), 0.1, 50)

    glTranslatef (0, 0, -5)

    Clock = pygame.time.Clock ()
    while True:
        Clock.tick (60)

        for Event in pygame.event.get ():
            if Event.type == pygame.QUIT:
                pygame.quit ()
                quit ()

        glRotatef (2, 1, 1, 3)
        #glRotatef (2, 0, 0, 1)
        glClear (GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        Draw (Vertices, Edges)

        pygame.display.flip ()

#Run ()
