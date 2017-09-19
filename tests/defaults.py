

class Header:

    # Allowed SingularityApp header fields
    allowed = ['author', 'date', 'files', 'tags', 'title']

    # Required SingularityApp header fields
    required = ['author', 'date', 'tags', 'title']

    # Operating system options (one or more must be present)
    oses = ['ubuntu', 'debian', 'centos', 'redhat', 'linux']

class Sections:

    # Allowed SingularityApp header fields
    allowed = ['apphelp',
               'appinstall',
               'applabels',
               'appenv',
               'apprun']
