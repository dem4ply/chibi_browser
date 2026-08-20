import logging
import datetime
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import SessionNotCreatedException
from chibi_browser.web_element import Chibi_web_element

from chibi.file.temp import Chibi_temp_path
from chibi.file import Chibi_path
from chibi.config import configuration


logger = logging.getLogger( 'chibi_browser.snipepts' )


def build_options( download_folder=None, options=None ):
    if options is None:
        from selenium.webdriver.chrome.options import Options
        options = Options()
    pref = {}
    if download_folder:
        pref.update( {
            "download.default_directory": download_folder,
            "savefile.default_directory": download_folder,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
        } )
        options.add_argument( '--handle_prefs' )
        options.add_argument( "--disable-popup-blocking" )
        options.add_argument( "--disable-web-security" )

    options.add_argument("--disable-notifications")
    options.add_argument("--disable-render-loop")
    options.add_argument("--disable-gpu")
    default_content_settings = (
        configuration.chibi_browser.default_content_settings )
    if default_content_settings:
        if default_content_settings.images:
            images = default_content_settings.images
            options.add_argument("--blink-settings=imagesEnabled=true")
        else:
            images = 2
            options.add_argument("--blink-settings=imagesEnabled=false")
    else:
        images = 2
        options.add_argument("--blink-settings=imagesEnabled=false")
    pref.update( {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
        "profile.managed_default_content_settings.images": images,
    } )
    options.add_experimental_option( 'prefs', pref )
    return options


def build_options_undetected( download_folder=None ):
    # from undetected_chromedriver.options import ChromeOptions as Options
    from undetected.options import ChromeOptions as Options
    options = Options()
    options = build_options( download_folder=download_folder, options=options )
    return options


def build_chrome( *args, download_folder=None, detach=False ):

    options = build_options( download_folder=download_folder )
    default_debugger_port = "9222"
    default_debugger_address = f"127.0.0.1:{default_debugger_port}"
    if detach:
        # options.add_experimental_option( 'detach', detach )
        options.add_experimental_option(
            "debuggerAddress", default_debugger_address )
        try:
            logger.info(
                "intentado de connectar con chrome usando "
                f"el la direcion {default_debugger_port}"
            )
            driver = webdriver.Chrome( options=options )
            logger.info(
                f"conecion exitosa con la direcion {default_debugger_port}"
            )
        except SessionNotCreatedException:
            logger.info(
                f"no se pudo conectar a chrome en {default_debugger_address},"
                " se creara una nueva sesion" )
            options = build_options( download_folder=download_folder )
            options.add_experimental_option( 'detach', detach )
            options.add_argument(
                f"--remote-debugging-port={default_debugger_port}" )
            driver = webdriver.Chrome( options=options )
            driver._web_element_cls = Chibi_web_element
    else:
        # options.add_argument( "--headless=new" )
        driver = webdriver.Chrome( options=options )
        driver._web_element_cls = Chibi_web_element
    return driver


def force_patcher_to_use_undetected( directory ):
    # source:
    # https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/528
    import undetected_chromedriver as uc
    # copy the chromedriver in directory
    exe = uc.Patcher.exe_name % ""
    exe = f"undetected_{exe}"
    src = Chibi_path( uc.Patcher.data_path )
    src = src + exe
    # src = os.path.join(uc.Patcher.data_path, exe)
    # executable_path = os.path.join(directory, exe)
    executable_path = directory + exe
    src.copy( executable_path )
    # shutil.copyfile(src, executable_path)

    # monkey patch the Patcher class
    class PatcherWithForcedExecutablePath( uc.Patcher ):
        def __init__( self, *args, **kw ):
            kw[ "executable_path" ] = executable_path
            super().__init__( *args, **kw )

    uc.Patcher = PatcherWithForcedExecutablePath

    return executable_path


def build_undetected_chrome( *args, download_folder=None, detach=False ):
    # import undetected as uc
    default_debugger_port = "9322"
    default_debugger_address = f"127.0.0.1:{default_debugger_port}"
    try:
        import undetected as uc
        # import undetected_chromedriver as uc
        # from undetected_chromedriver.options import ChromeOptions as Options
    except ImportError:
        logger.exception( (
            'se nesesita instalar undetected_chromedriver '
            '"pip install undetected_chromedriver"' ) )
        raise

    options = build_options_undetected( download_folder=download_folder )

    # options.add_argument( "--headless=new" )
    desire_capabilities = DesiredCapabilities.CHROME
    desire_capabilities[ 'pageLoadStrategy' ] = 'eager'

    if detach:
        # options.add_experimental_option( 'detach', detach )
        options.add_experimental_option(
            "debuggerAddress", default_debugger_address )
        options.debugger_address = default_debugger_address
        try:
            logger.info(
                "intentado de connectar con chrome usando "
                f"el la direcion {default_debugger_port}"
            )
            if configuration.chibi_browser.user_profile_path:
                user_profile_path = (
                    configuration.chibi_browser.user_profile_path )
            driver = uc.Chrome(
                options=options, user_data_dir=user_profile_path )
            logger.info(
                f"conecion exitosa con la direcion {default_debugger_port}"
            )
        except SessionNotCreatedException:
            logger.info(
                f"no se pudo conectar a chrome en {default_debugger_address},"
                " se creara una nueva sesion" )
            options = build_options_undetected(
                download_folder=download_folder )
            options.add_experimental_option( 'detach', detach )
            options.add_argument(
                f"--remote-debugging-port={default_debugger_port}" )
            driver = uc.Chrome( options=options, )
    else:
        # options.add_argument( "--headless=new" )
        if configuration.chibi_browser.user_profile_path:
            user_profile_path = (
                configuration.chibi_browser.user_profile_path )
        else:
            user_profile_path = None
        driver = uc.Chrome(
            options=options, user_data_dir=user_profile_path )

    driver._web_element_cls = Chibi_web_element
    return driver


def build_driver( *args, **kw ):
    try:
        return build_undetected_chrome( *args, **kw )
        # return build_chrome( *args, **kw )
    except ImportError:
        logger.exception(
            "no se pudo usar undetected chrome se usara chrome regular" )
        return build_chrome( *args, **kw )


def wait_to_browser_close( browser, timeout=None ):
    start = datetime.datetime.utcnow()
    from chibi_browser import Chibi_browser
    if isinstance( browser, Chibi_browser ):
        browser = browser.browser
    while True:
        try:
            _ = browser.window_handles
        except selenium.common.exceptions.InvalidSessionIdException:
            logger.info( "se detecto que el navegador fue cerrado" )
            break
        time.sleep( 1 )
        if timeout:
            current = datetime.datetime.utcnow()
            delta = current - start
            if delta.total_seconds() > timeout:
                break


js_code_for_hide_mouse = """
var seleniumFollowerImg = document.getElementById( "selenium_mouse_follower" )

if ( seleniumFollowerImg !== undefined )
    seleniumFollowerImg.style.display = 'none'
    """

js_code_for_mouse = """
var seleniumFollowerImg = document.getElementById( "selenium_mouse_follower" )

if ( seleniumFollowerImg !== undefined )
{
    var seleniumFollowerImg = document.createElement("img");
    seleniumFollowerImg.setAttribute('src', 'data:image/png;base64,'
        + 'iVBORw0KGgoAAAANSUhEUgAAABQAAAAeCAQAAACGG/bgAAAAAmJLR0QA'
        + '/4ePzL8AAAAJcEhZcwAA'
        + 'HsYAAB7GAZEt8iwAAAAHdElNRQfgAwgMIwdxU/i7AAABZklEQVQ4y43TsU4UURSH'
        + '8W+XmYwkS2I0'
        + '9CRKpKGhsvIJjG9giQmliHFZlkUIGnEF7KTiCagpsYHWhoTQaiUUxL'
        + 'ixYZb5KAAZZhbunu7O/PKf'
        + 'e+fcA+/pqwb4DuximEqXhT4iI8dMpBWEsWsu'
        + 'GYdpZFttiLSSgTvhZ1W/SvfO1CvYdV1kPghV68a3'
        + '0zzUWZH5pBqEui7dnqlFmLoq0gxC1XfGZd'
        + 'oLal2kea8ahLoqKXNAJQBT2yJzwUTVt0bS6ANqy1ga'
        + 'VCEq/oVTtjji4hQVhhnlYBH4WIJV9v'
        + 'lkXLm+10R8oJb79Jl1j9UdazJRGpkrmNkSF9SOz2T71s7M'
        + 'SIfD2lmmfjGSRz3hK8l4w1P+bah/HJL'
        + 'N0sys2JSMZQB+jKo6KSc8vLlLn5ikzF4268Wg2+pPOWW6'
        + 'ONcpr3PrXy9VfS473M/D7H+TLmrqsX'
        + 'tOGctvxvMv2oVNP+Av0uHbzbxyJaywyUjx8TlnPY2YxqkD'
        + 'dAAAAABJRU5ErkJggg==');

    seleniumFollowerImg.setAttribute('id', 'selenium_mouse_follower');
    seleniumFollowerImg.setAttribute(
        'style', 'position: absolute; z-index: 99999999999;'
        + 'pointer-events: none;' );
    document.body.appendChild(seleniumFollowerImg);

    document.onmousemove = function(e) {
        const mousePointer = document.getElementById(
            'selenium_mouse_follower');
        mousePointer.style.left = e.pageX + 'px';
        mousePointer.style.top = e.pageY + 'px';
    }
}
    """


def add_mouse_to_selenium( driver ):
    driver.execute_script( js_code_for_mouse )


def hide_mouse_to_selenium( driver ):
    driver.execute_script( js_code_for_hide_mouse )


js_get_all_attrs = """
var items = {};
for (var i = 0; i < arguments[0].attributes.length; i++) {
    items[arguments[0].attributes[i].name] = arguments[0].attributes[i].value;
};
return items;
"""
