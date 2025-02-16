"""Fixtures for Discovergy integration tests."""
from unittest.mock import AsyncMock, patch

from pydiscovergy import Discovergy
from pydiscovergy.models import Reading
import pytest

from homeassistant.components.discovergy import DOMAIN
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component

from tests.common import MockConfigEntry
from tests.components.discovergy.const import GET_METERS, LAST_READING, LAST_READING_GAS


def _meter_last_reading(meter_id: str) -> Reading:
    """Side effect function for Discovergy mock."""
    return (
        LAST_READING_GAS
        if meter_id == "d81a652fe0824f9a9d336016587d3b9d"
        else LAST_READING
    )


@pytest.fixture(name="discovergy")
def mock_discovergy() -> None:
    """Mock the pydiscovergy client."""
    mock = AsyncMock(spec=Discovergy)
    mock.meters.return_value = GET_METERS
    mock.meter_last_reading.side_effect = _meter_last_reading

    with patch(
        "homeassistant.components.discovergy.pydiscovergy.Discovergy",
        return_value=mock,
    ):
        yield mock


@pytest.fixture(name="config_entry")
async def mock_config_entry(hass: HomeAssistant) -> MockConfigEntry:
    """Return a MockConfigEntry for testing."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="user@example.org",
        unique_id="user@example.org",
        data={CONF_EMAIL: "user@example.org", CONF_PASSWORD: "supersecretpassword"},
    )


@pytest.fixture(name="setup_integration")
async def mock_setup_integration(
    hass: HomeAssistant, config_entry: MockConfigEntry, discovergy: AsyncMock
) -> None:
    """Fixture for setting up the component."""
    config_entry.add_to_hass(hass)

    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()
