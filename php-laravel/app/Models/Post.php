<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    use HasFactory;

    protected $fillable = ['title', 'body', 'published_at'];

    protected $dates = ['published_at'];

    public function getTitleAttribute($value)
    {
        return ucfirst($value);
    }

    public function getPublishedAgoAttribute()
    {
        return $this->published_at ? $this->published_at->diffForHumans() : null;
    }
}
