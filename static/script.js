(function() {
    const theme = localStorage.getItem('theme') || 'auto';
    if (theme !== 'auto') {
        document.documentElement.setAttribute('data-theme', theme);
    }
    window.initialTheme = theme;
})();

document.addEventListener('DOMContentLoaded', function() {
    // Theme switcher functionality
    const themeSelect = document.getElementById('theme-select');
    themeSelect.value = localStorage.getItem('theme') || 'auto';
    
    function updateBanner(theme) {
        const isLcars = theme === 'lcars';
        // For now, Material 3 theme uses the default banner
        const bannerType = isLcars ? 'lcars' : 'banner';
        
        document.getElementById('banner-small').srcset = `assets/${bannerType}-small.webp`;
        document.getElementById('banner-medium').srcset = `assets/${bannerType}-medium.webp`;
        document.getElementById('banner-large').src = `assets/${bannerType}-large.webp`;
    }
    
    themeSelect.addEventListener('change', (e) => {
        const theme = e.target.value;
        localStorage.setItem('theme', theme);
        if (theme === 'auto') {
            document.documentElement.removeAttribute('data-theme');
            updateBanner('auto');
        } else {
            document.documentElement.setAttribute('data-theme', theme);
            updateBanner(theme);
        }
    });
    
    updateBanner(window.initialTheme || themeSelect.value);
    
    // Sidebar functionality
    const postListSidebar = document.getElementById('post-list-sidebar');
    const tagCloud = document.getElementById('tag-cloud');
    const clearFiltersBtn = document.getElementById('clear-filters');
    
    if (!postListSidebar || !tagCloud) return; // Skip if we're not on a page with the sidebar
    
    // Get all posts from the main content
    function getAllPosts() {
        const posts = [];
        const postElements = document.querySelectorAll('.post-list li');
        
        postElements.forEach(post => {
            const titleEl = post.querySelector('h3 a');
            const dateEl = post.querySelector('.post-meta');
            const tagsEl = post.querySelectorAll('.tag');
            
            if (titleEl) {
                const tags = [];
                tagsEl.forEach(tag => tags.push(tag.textContent.trim()));
                
                posts.push({
                    title: titleEl.textContent,
                    url: titleEl.getAttribute('href'),
                    date: dateEl ? dateEl.textContent.trim() : '',
                    tags: tags,
                    element: post
                });
            }
        });
        
        return posts;
    }
    
    // Populate sidebar post list
    function populateSidebarPosts(posts) {
        if (!posts || posts.length === 0) {
            postListSidebar.innerHTML = '<p>No posts found</p>';
            return;
        }
        
        const ul = document.createElement('ul');
        
        posts.forEach(post => {
            const li = document.createElement('li');
            li.innerHTML = `
                <a href="${post.url}">${post.title}</a>
                <div class="post-date">${post.date}</div>
            `;
            ul.appendChild(li);
        });
        
        postListSidebar.innerHTML = '';
        postListSidebar.appendChild(ul);
    }
    
    // Extract all unique tags
    function extractTags(posts) {
        const tagSet = new Set();
        
        posts.forEach(post => {
            post.tags.forEach(tag => tagSet.add(tag));
        });
        
        return Array.from(tagSet).sort();
    }
    
    // Populate tag cloud
    function populateTagCloud(tags) {
        if (!tags || tags.length === 0) {
            tagCloud.innerHTML = '<p>No tags found</p>';
            return;
        }
        
        tagCloud.innerHTML = '';
        
        tags.forEach(tag => {
            const tagEl = document.createElement('span');
            tagEl.className = 'tag';
            tagEl.textContent = tag;
            tagEl.dataset.tag = tag;
            tagEl.addEventListener('click', () => toggleTagFilter(tag));
            tagCloud.appendChild(tagEl);
        });
    }
    
    // Filter posts by selected tags and search query
    let selectedTags = [];
    let searchQuery = '';
    
    function toggleTagFilter(tag) {
        const index = selectedTags.indexOf(tag);
        
        if (index === -1) {
            // Add tag to filter
            selectedTags.push(tag);
        } else {
            // Remove tag from filter
            selectedTags.splice(index, 1);
        }
        
        updateTagCloudUI();
        filterPosts();
    }
    
    // Search functionality
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            searchQuery = e.target.value.toLowerCase().trim();
            filterPosts();
        });
    }
    
    function updateTagCloudUI() {
        // Update tag cloud UI to show selected tags
        document.querySelectorAll('#tag-cloud .tag').forEach(tagEl => {
            if (selectedTags.includes(tagEl.dataset.tag)) {
                tagEl.classList.add('active');
            } else {
                tagEl.classList.remove('active');
            }
        });
    }
    
    function filterPosts() {
        const posts = getAllPosts();
        
        posts.forEach(post => {
            // Check if post matches tag filter
            const matchesTags = selectedTags.length === 0 || 
                               selectedTags.every(tag => post.tags.includes(tag));
            
            // Check if post matches search query
            const matchesSearch = searchQuery === '' || 
                                 post.title.toLowerCase().includes(searchQuery) || 
                                 post.tags.some(tag => tag.toLowerCase().includes(searchQuery));
            
            // Show post only if it matches both filters
            if (matchesTags && matchesSearch) {
                post.element.classList.remove('hidden');
            } else {
                post.element.classList.add('hidden');
            }
        });
        
        // Update UI to show how many posts are visible
        const visibleCount = posts.filter(post => !post.element.classList.contains('hidden')).length;
        const totalCount = posts.length;
        
        // If we have a heading element before the post list, update it
        const headingEl = document.querySelector('.post-list').previousElementSibling;
        if (headingEl && headingEl.tagName === 'H2') {
            if (visibleCount < totalCount) {
                headingEl.textContent = `Showing ${visibleCount} of ${totalCount} Posts`;
            } else {
                headingEl.textContent = 'All Posts';
            }
        }
    }
    
    // Clear all filters
    clearFiltersBtn.addEventListener('click', () => {
        selectedTags = [];
        if (searchInput) {
            searchInput.value = '';
            searchQuery = '';
        }
        updateTagCloudUI();
        filterPosts();
    });
    
    // Table of Contents functionality
    function generateTableOfContents() {
        const tocContainer = document.getElementById('table-of-contents');
        if (!tocContainer) return;
        
        const article = document.querySelector('article');
        if (!article) return;
        
        const headings = article.querySelectorAll('h2, h3, h4');
        if (headings.length === 0) {
            tocContainer.innerHTML = '<p>No headings found</p>';
            return;
        }
        
        const toc = document.createElement('ul');
        let currentLevel = 2;
        let currentList = toc;
        let listStack = [toc];
        
        headings.forEach((heading, index) => {
            // Add id to heading if it doesn't have one
            if (!heading.id) {
                heading.id = `heading-${index}`;
            }
            
            const level = parseInt(heading.tagName.substring(1));
            
            // Create list item
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = `#${heading.id}`;
            a.textContent = heading.textContent;
            a.addEventListener('click', (e) => {
                e.preventDefault();
                heading.scrollIntoView({ behavior: 'smooth' });
                window.history.pushState(null, null, `#${heading.id}`);
            });
            li.appendChild(a);
            
            // Handle nesting
            if (level > currentLevel) {
                // Create a new nested list
                const nestedList = document.createElement('ul');
                listStack[listStack.length - 1].lastChild.appendChild(nestedList);
                listStack.push(nestedList);
                currentList = nestedList;
                currentLevel = level;
            } else if (level < currentLevel) {
                // Go back up the stack
                while (level < currentLevel && listStack.length > 1) {
                    listStack.pop();
                    currentLevel--;
                }
                currentList = listStack[listStack.length - 1];
            }
            
            currentList.appendChild(li);
        });
        
        tocContainer.innerHTML = '';
        tocContainer.appendChild(toc);
        
        // Add scroll spy functionality
        const tocLinks = tocContainer.querySelectorAll('a');
        
        const headingElements = Array.from(headings);
        let activeHeadingIndex = -1;
        
        function updateActiveTocLink() {
            const scrollPosition = window.scrollY + 100; // Offset for better UX
            
            // Find the current active heading
            let newActiveIndex = -1;
            for (let i = 0; i < headingElements.length; i++) {
                if (headingElements[i].offsetTop <= scrollPosition) {
                    newActiveIndex = i;
                } else {
                    break;
                }
            }
            
            // Update active class if needed
            if (newActiveIndex !== activeHeadingIndex) {
                activeHeadingIndex = newActiveIndex;
                
                // Remove active class from all links
                tocLinks.forEach(link => link.classList.remove('active'));
                
                // Add active class to current link
                if (activeHeadingIndex >= 0) {
                    tocLinks[activeHeadingIndex].classList.add('active');
                }
            }
        }
        
        // Initial update
        updateActiveTocLink();
        
        // Update on scroll
        window.addEventListener('scroll', updateActiveTocLink);
    }
    
    // Initialize sidebar
    const posts = getAllPosts();
    const tags = extractTags(posts);
    
    populateSidebarPosts(posts);
    populateTagCloud(tags);
    generateTableOfContents();
});