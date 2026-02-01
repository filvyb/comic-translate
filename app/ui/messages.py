from .dayu_widgets.message import MMessage
from PySide6.QtCore import QCoreApplication, Qt
from PySide6 import QtWidgets

# Shorthand for translations
_translate = QCoreApplication.translate

class Messages:

    @staticmethod
    def show_translation_complete(parent):

        MMessage.success(
            text=_translate(
                "Messages", 
                "Comic has been Translated!"
            ),
            parent=parent,
            duration=None,
            closable=True
        )

    @staticmethod
    def select_font_error(parent):
        MMessage.error(
            text=_translate(
                "Messages", 
                "No Font selected.\nGo to Settings > Text Rendering > Font to select or import one "
            ),
            parent=parent,
            duration=None,
            closable=True
        )

    @staticmethod
    def show_not_logged_in_error(parent):
        MMessage.error(
            text=_translate(
                "Messages",
                "Please provide API credentials in Settings > Credentials to continue."
            ),
            parent=parent,
            duration=None,
            closable=True
        )

    @staticmethod
    def show_translator_language_not_supported(parent):
        MMessage.error(
            text=_translate(
                "Messages",
                "The translator does not support the selected target language. Please choose a different language or tool."
            ),
            parent=parent,
            duration=None,
            closable=True
        )

    @staticmethod
    def show_missing_tool_error(parent, tool_name):
        MMessage.error(
            text=_translate(
                "Messages",
                "No {} selected. Please select a {} in Settings > Tools."
            ).format(tool_name, tool_name),
            parent=parent,
            duration=None,
            closable=True
        )

    @staticmethod
    def show_error_with_copy(parent, title: str, text: str, detailed_text: str | None = None):
        """
        Show a critical error dialog where the main text is selectable and the
        full details (traceback) are placed in the Details pane. A Copy button
        is provided to copy the full details to the clipboard.

        Args:
            parent: parent widget
            title: dialog window title
            text: short error text shown in the main area
            detailed_text: optional long text (traceback) shown in Details
        """
        msg = QtWidgets.QMessageBox(parent)
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(text)
        if detailed_text:
            msg.setDetailedText(detailed_text)

        # Allow selecting the main text
        try:
            msg.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        except Exception:
            pass

        copy_btn = msg.addButton(QCoreApplication.translate("Messages", "Copy"), QtWidgets.QMessageBox.ActionRole)
        # Add standard buttons so the window has a RejectRole (Close) and AcceptRole (Ok)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Close)
        msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
        msg.exec()

        if msg.clickedButton() == copy_btn:
            try:
                QtWidgets.QApplication.clipboard().setText(detailed_text or text)
            except Exception:
                pass

    @staticmethod
    def show_server_error(parent, status_code: int = 500):
        """
        Show a user-friendly error for 5xx server issues.
        """
        messages = {
            500: _translate("Messages", "An unexpected error occurred on the server.\nPlease try again later."),
            501: _translate("Messages", "The selected translator is currently unavailable.\nPlease select a different tool in Settings."),
            502: _translate("Messages", "The server received an invalid response from an upstream provider.\nPlease try again later."),
            503: _translate("Messages", "The server is currently unavailable or overloaded.\nPlease try again later."),
            504: _translate("Messages", "The server timed out waiting for a response.\nPlease try again later."),
        }
        text = messages.get(status_code, messages[500])
        
        MMessage.error(
            text=text,
            parent=parent,
            duration=None,
            closable=True
        )

    @staticmethod
    def show_network_error(parent):
        """
        Show a user-friendly error for network/connectivity issues.
        """
        MMessage.error(
            text=_translate(
                "Messages", 
                "Unable to connect to the server.\nPlease check your internet connection."
            ),
            parent=parent,
            duration=None,
            closable=True
        )

    @staticmethod
    def show_content_flagged_error(parent):
        """
        Show a friendly error when content is blocked by safety filters.
        """
        MMessage.error(
            text=_translate(
                "Messages", 
                "Translation blocked: The content was flagged by safety filters.\nPlease try modifying the text or using a different translator."
            ),
            parent=parent,
            duration=None,
            closable=True
        )

