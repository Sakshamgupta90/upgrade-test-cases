<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;

class PostController extends Controller
{
    public function store(Request $request)
    {
        $data = $this->validate($request, [
            'title' => 'required|string|max:255',
            'body' => 'required|string',
            'published_at' => 'nullable|date',
        ]);

        $post = Post::create($data);

        return redirect()->route('posts.show', $post);
    }

    public function export(Post $post)
    {
        $path = "exports/post-{$post->id}.txt";
        Storage::disk('local')->put($path, $post->body);

        $absolute = Storage::disk('local')->getDriver()->getAdapter()->getPathPrefix() . $path;

        return response()->download($absolute);
    }
}
