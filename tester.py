import pytest
import Plotter

@pytest.fixture
def app(qtbot):
    test = Plotter.MainWindow()
    qtbot.addWidget(test)
    return test

def test_QLineEdit(app, qtbot):

    # test if empty input
    app.function_input.setText('')
    app.button_to_conv.click()
    assert app.error == "Enter a function to plot!"

    # test if invalid variables was given
    app.function_input.setText('abc')
    app.button_to_conv.click()
    assert app.error == "'abc' is not in the allowed as an input character!"


def test_submit_text(app):
    assert app.button_to_conv.text() == "Plot"

# Test range prefixes
def test_range_prefixes(app, qtbot):
    assert app.min_input.prefix() == "Min value: "
    assert app.max_input.prefix() == "Max value: "
    app.function_input.setText('x')
    app.min_input.setValue(10)
    app.max_input.setValue(4)
    assert app.error == "Maximum input must be bigger than Minimum input"


#test range change
def test_range_changes(app):
    app.min_input.stepBy(15)
    assert app.min_input.value() == 5.0
    app.max_input.stepBy(-15)
    assert app.max_input.value() == 6.0


