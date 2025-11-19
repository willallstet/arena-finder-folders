import html
import io
import re
from pathlib import Path
from typing import Any, Self

import httpx

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None  # type: ignore

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None  # type: ignore

from pydantic import BaseModel, Field

from beeai_framework.context import RunContext
from beeai_framework.emitter.emitter import Emitter
from beeai_framework.tools.errors import ToolError
from beeai_framework.tools.search import SearchToolOutput, SearchToolResult
from beeai_framework.tools.tool import Tool
from beeai_framework.tools.types import ToolRunOptions


class ArenaToolInput(BaseModel):
    user_id: str = Field(description="The Are.na user ID or username to fetch channels from.")
    access_token: str = Field(
        description="Are.na API access token. Required for authentication. Get one from https://dev.are.na/oauth/applications",
    )


class ArenaToolResult(SearchToolResult):
    pass


class ArenaToolOutput(SearchToolOutput):
    pass


class ArenaTool(Tool[ArenaToolInput, ToolRunOptions, ArenaToolOutput]):
    name = "Are.na"
    description = "Fetch all block titles from a user's Are.na channels, including channels they don't own."
    input_schema = ArenaToolInput
    _base_url = "https://api.are.na/v2"

    def _create_emitter(self) -> Emitter:
        return Emitter.root().child(
            namespace=["tool", "search", "arena"],
            creator=self,
        )

    async def clone(self) -> Self:
        tool = self.__class__(options=self.options)
        tool.name = self.name
        tool.description = self.description
        tool.input_schema = self.input_schema
        tool.middlewares.extend(self.middlewares)
        tool._cache = await self.cache.clone()
        return tool

    async def _fetch_user_channels(
        self, client: httpx.AsyncClient, user_id: str, access_token: str
    ) -> list[dict[str, Any]]:
        """Fetch all channels for a user."""
        headers = {"Authorization": f"Bearer {access_token}"}

        all_channels = []
        page = 1
        per_page = 100

        while True:
            url = f"{self._base_url}/users/{user_id}/channels"
            params = {"page": page, "per": per_page}

            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            channels = data.get("channels", [])
            if not channels:
                break

            all_channels.extend(channels)

            # Check if there are more pages
            if len(channels) < per_page:
                break
            page += 1

        return all_channels

    async def _fetch_channel_blocks(
        self, client: httpx.AsyncClient, channel_slug: str, access_token: str
    ) -> list[dict[str, Any]]:
        """Fetch all blocks from a channel."""
        headers = {"Authorization": f"Bearer {access_token}"}

        all_blocks = []
        page = 1
        per_page = 100

        while True:
            url = f"{self._base_url}/channels/{channel_slug}/contents"
            params = {"page": page, "per": per_page}

            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            blocks = data.get("contents", [])
            if not blocks:
                break

            all_blocks.extend(blocks)

            # Check if there are more pages
            if len(blocks) < per_page:
                break
            page += 1

        return all_blocks

    def _save_text_blocks(self, blocks: list[dict[str, Any]]) -> None:
        """Save Text block content as markdown files in arena_content folder."""
        # Create arena_content directory if it doesn't exist
        content_dir = Path("arena_content")
        content_dir.mkdir(exist_ok=True)
        
        for block in blocks:
            if block.get("class") == "Text":
                content = block.get("content")
                if not content:
                    continue
                
                # Generate filename from block ID or title
                block_id = block.get("id")
                title = block.get("title", "untitled")
                
                # Sanitize title for filename (remove invalid characters)
                safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).strip()
                safe_title = safe_title.replace(" ", "_")[:50]  # Limit length
                
                if block_id:
                    filename = f"{block_id}_{safe_title}.md" if safe_title else f"{block_id}.md"
                else:
                    filename = f"{safe_title}.md" if safe_title else "untitled.md"
                
                filepath = content_dir / filename
                
                # Write content to file
                try:
                    filepath.write_text(content, encoding="utf-8")
                except Exception as e:
                    # Log error but continue processing other blocks
                    import sys
                    print(f"Error saving block {block_id}: {e}", file=sys.stderr)

    async def _save_attachment_blocks(
        self, blocks: list[dict[str, Any]], client: httpx.AsyncClient
    ) -> None:
        """Download PDF attachments from source URLs and extract text as markdown files."""
        if PdfReader is None:
            import sys
            print(
                "Warning: pypdf not installed. Cannot extract text from PDFs. "
                "Install with: pip install pypdf",
                file=sys.stderr,
            )
            return

        # Create arena_content directory if it doesn't exist
        content_dir = Path("arena_content")
        content_dir.mkdir(exist_ok=True)

        for block in blocks:
            if block.get("class") == "Attachment":
                # Check if it's a PDF
                title = block.get("title", "")
                if not title or not title.lower().endswith(".pdf"):
                    continue

                # Get source URL
                source = block.get("source")
                if not source:
                    continue

                source_url = source.get("url")
                if not source_url:
                    continue

                block_id = block.get("id")
                if not block_id:
                    continue

                # Download PDF
                try:
                    response = await client.get(source_url, timeout=60.0, follow_redirects=True)
                    response.raise_for_status()

                    # Check if it's actually a PDF
                    content_type = response.headers.get("content-type", "").lower()
                    if "pdf" not in content_type and not source_url.lower().endswith(".pdf"):
                        continue

                    # Extract text from PDF
                    pdf_bytes = response.content
                    pdf_file = io.BytesIO(pdf_bytes)
                    pdf_reader = PdfReader(pdf_file)

                    # Extract text from all pages
                    extracted_text = []
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            extracted_text.append(page_text)

                    if not extracted_text:
                        continue

                    content = "\n\n".join(extracted_text)

                    # Generate filename
                    safe_title = "".join(
                        c for c in title if c.isalnum() or c in (" ", "-", "_", ".")
                    ).strip()
                    safe_title = safe_title.replace(" ", "_")[:50]  # Limit length

                    filename = f"{block_id}_{safe_title}.md" if safe_title else f"{block_id}.md"
                    filepath = content_dir / filename

                    # Write content to file
                    filepath.write_text(content, encoding="utf-8")

                except Exception as e:
                    # Log error but continue processing other blocks
                    import sys

                    print(
                        f"Error processing PDF attachment {block_id} from {source_url}: {e}",
                        file=sys.stderr,
                    )
                    continue

    def _extract_text_from_html(self, html_content: str) -> str:
        """Extract plain text from HTML, focusing on main content and excluding navigation."""
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Remove script, style, and other non-content elements
        for element in soup(["script", "style", "meta", "link", "head", "nav", "header", "footer", "aside"]):
            element.decompose()
        
        # Try to find main content area
        main_content = None
        
        # First, try semantic HTML5 tags
        main_content = soup.find("main") or soup.find("article")
        
        # If not found, try common content container IDs
        if not main_content:
            for content_id in ["content", "main", "main-content", "article", "post", "entry", "story", "article-body"]:
                main_content = soup.find(id=content_id)
                if main_content:
                    break
        
        # If still not found, try common content container classes
        if not main_content:
            for content_class in ["content", "main", "main-content", "article", "post", "entry", "story", "article-body", "post-content"]:
                main_content = soup.find(class_=content_class)
                if main_content:
                    break
        
        # If we found a main content area, use it; otherwise use body
        if main_content:
            # Remove any remaining navigation elements within the content
            for nav in main_content.find_all(["nav", "header", "footer", "aside"]):
                nav.decompose()
            text = main_content.get_text()
        else:
            # Fallback to body, but remove navigation elements
            body = soup.find("body")
            if body:
                for nav in body.find_all(["nav", "header", "footer", "aside"]):
                    nav.decompose()
                text = body.get_text()
            else:
                text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        cleaned_text = "\n".join(chunk for chunk in chunks if chunk)
        
        return cleaned_text

    async def _save_link_blocks(
        self, blocks: list[dict[str, Any]], client: httpx.AsyncClient
    ) -> None:
        """Download web pages from Link blocks and extract text as markdown files."""
        # Create arena_content directory if it doesn't exist
        content_dir = Path("arena_content")
        content_dir.mkdir(exist_ok=True)

        for block in blocks:
            if block.get("class") == "Link":
                # Get source URL
                source = block.get("source")
                if not source:
                    # Fallback to block's url field if source is not available
                    source_url = block.get("url")
                else:
                    source_url = source.get("url")

                if not source_url:
                    continue

                block_id = block.get("id")
                if not block_id:
                    continue

                title = block.get("title", "untitled")

                # Download web page
                try:
                    response = await client.get(
                        source_url, timeout=60.0, follow_redirects=True, headers={"User-Agent": "Mozilla/5.0"}
                    )
                    response.raise_for_status()

                    # Check if it's HTML
                    content_type = response.headers.get("content-type", "").lower()
                    if "html" not in content_type:
                        continue

                    # Extract text from HTML
                    html_content = response.text
                    content = self._extract_text_from_html(html_content)

                    if not content or len(content.strip()) < 10:  # Skip if too short
                        continue

                    # Generate filename
                    safe_title = "".join(
                        c for c in title if c.isalnum() or c in (" ", "-", "_")
                    ).strip()
                    safe_title = safe_title.replace(" ", "_")[:50]  # Limit length

                    filename = f"{block_id}_{safe_title}.md" if safe_title else f"{block_id}.md"
                    filepath = content_dir / filename

                    # Write content to file
                    filepath.write_text(content, encoding="utf-8")

                except Exception as e:
                    # Log error but continue processing other blocks
                    import sys

                    print(
                        f"Error processing link {block_id} from {source_url}: {e}",
                        file=sys.stderr,
                    )
                    continue

    async def _run(
        self, input: ArenaToolInput, options: ToolRunOptions | None, context: RunContext
    ) -> ArenaToolOutput:
        results: list[SearchToolResult] = []

        async with httpx.AsyncClient(timeout=30.0) as client:
            # Fetch all channels for the user
            try:
                channels = await self._fetch_user_channels(client, input.user_id, input.access_token)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 401:
                    raise ToolError(
                        f"Authentication failed. Please check your access token is valid. "
                        f"Get an access token from https://dev.are.na/oauth/applications"
                    ) from e
                raise ToolError(f"Failed to fetch channels for user {input.user_id}: {e}") from e
            except httpx.HTTPError as e:
                raise ToolError(f"Failed to fetch channels for user {input.user_id}: {e}") from e

            # Fetch blocks from each channel
            for channel in channels:
                channel_slug = channel.get("slug")
                channel_title = channel.get("title", channel_slug or "Untitled Channel")
                channel_url = channel.get("url", f"https://are.na/{channel_slug}")

                if not channel_slug:
                    continue

                try:
                    blocks = await self._fetch_channel_blocks(client, channel_slug, input.access_token)
                    
                    # Filter blocks
                    filtered_blocks = []
                    for block in blocks:
                        # Skip Embed blocks
                        if block.get("class") == "Media":
                            continue
                        if block.get("class") == "Attachment" and block.get("title") and block.get("title")[-4:] != ".pdf":
                            continue
                        if block.get("class") == "Image":
                            continue
                        filtered_blocks.append(block)
                    
                    # Save Text blocks as markdown files
                    self._save_text_blocks(filtered_blocks)
                    
                    # Save PDF Attachment blocks as markdown files (extract text from source)
                    await self._save_attachment_blocks(filtered_blocks, client)
                    
                    # Save Link blocks as markdown files (extract text from web pages)
                    await self._save_link_blocks(filtered_blocks, client)
                    
                    # Process filtered blocks for results
                    for block in filtered_blocks:
                        title = block.get("title")
                        if not title:
                            continue

                        # Get block description if available
                        description = block.get("description") or block.get("content") or f"Block from {channel_title}"
                        # Construct proper block URL: https://are.na/block/{block_id}
                        block_id = block.get("id")
                        if block_id:
                            block_url = f"https://are.na/block/{block_id}"
                        else:
                            # Fallback to block's url field if id is missing
                            block_url = block.get("url", channel_url)

                        results.append(
                            ArenaToolResult(
                                title=title,
                                description=description,
                                url=block_url,
                            )
                        )
                except httpx.HTTPError:
                    # Skip channels that fail to load (might be private or deleted)
                    continue

        return ArenaToolOutput(results)

