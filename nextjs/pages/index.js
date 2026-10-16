import Head from 'next/head';
import Image from 'next/image';
import Link from 'next/link';

export default function Home({ posts }) {
  return (
    <>
      <Head>
        <title>Blog</title>
      </Head>
      <div style={{ position: 'relative', height: 240 }}>
        <Image
          src="https://images.example.com/hero.jpg"
          alt="Hero"
          layout="fill"
          objectFit="cover"
        />
      </div>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>
            <Link href={`/posts/${post.id}`}>
              <a>{post.title}</a>
            </Link>
          </li>
        ))}
      </ul>
    </>
  );
}

Home.getInitialProps = async () => {
  const res = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=5');
  return { posts: await res.json() };
};
