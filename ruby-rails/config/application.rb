require_relative "boot"

require "rails/all"

Bundler.require(*Rails.groups)

module Blog
  class Application < Rails::Application
    config.load_defaults 6.1
    config.autoloader = :classic
    config.active_record.legacy_connection_handling = false
    config.time_zone = "UTC"
  end
end
