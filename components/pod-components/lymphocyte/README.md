### Lymphocyte container

Lymphocytes are the cells that make up the effector portion of the adaptive immune system; they are able to generate and modify antibodies that will recognize antigens in the future. Lymphocytes include natural killer cells (which function in cell-mediated, cytotoxic innate immunity), T cells (for cell-mediated, cytotoxic adaptive immunity), and B cells (for humoral, antibody-driven adaptive immunity). T Killer cells are specialised Lymphocytes that kills cancer cells, cells that are infected (particularly with viruses), or cells that are damaged in other ways.

In our SH setup a lymphocyte is a python docker container that runs together with a job container in a kubernetes pod. The lymphocyte container is inspired by T Killer cells. It decides if and when to send to the Docker Proxy the signal to kill (or pause or restart) the job container.
