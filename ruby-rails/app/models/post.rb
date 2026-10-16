class Post < ApplicationRecord
  enum status: [:draft, :published, :archived]
  serialize :tags, Array

  validates :title, presence: true

  scope :recent, -> { where("created_at > ?", 1.week.ago) }

  def published_label
    return "Not published" unless published_at

    "Published #{published_at.to_s(:long)}"
  end

  def api_key
    Rails.application.secrets.external_api_key
  end
end
