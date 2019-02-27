# PyFeedChecker

A cli and a lib to check feed sources for bad responses

## CLI

    $ python __main__.py -h
    usage: __main__.py [-h] [-i INPUT] [-o OUTPUT] [--timeout REQUEST_TIMEOUT]
                   [--oktimeout]
    optional arguments:
        -h, --help    show this help message and exit
        -i INPUT, --input INPUT    input path to check and filter
        -o OUTPUT, --output OUTPUT    output path
        --timeout REQUEST_TIMEOUT    request timeout seconds
        --oktimeout    considers a timeout response as a good response

## LIB

    from pyfeedchecker.feedchecker import Checker

    checker = Checker(input_path, output_path, request_timeout=10, timeout_is_bad=True)
    checker.run()
