import { describe, it, expect, vi } from 'vitest';
import { render, fireEvent } from '@testing-library/svelte';
import IconButton from '../../src/elements/IconButton.svelte';

describe('IconButton.svelte', () => {
  it('renders with default (not filled) classes when no props are passed', () => {
    const { getByRole } = render(IconButton);
    const button = getByRole('button');
    expect(button).toBeInTheDocument();
    expect(button.className).toContain('bg-white');
    expect(button.className).toContain('text-button');
    expect(button.className).toContain('border');
    expect(button.className).toContain('border-button');
    expect(button.className).toContain('rounded-md');
    expect(button.className).toContain('py-1');
    expect(button.className).toContain('px-2');
  });

  it('renders with default (not filled) classes when filled is false', () => {
    const { getByRole } = render(IconButton, { props: { filled: false } });
    const button = getByRole('button');
    expect(button).toBeInTheDocument();
    expect(button.className).toContain('bg-white');
    expect(button.className).toContain('text-button');
    expect(button.className).toContain('border');
  });

  it('renders with filled classes when filled is true', () => {
    const { getByRole } = render(IconButton, { props: { filled: true } });
    const button = getByRole('button');
    expect(button).toBeInTheDocument();
    expect(button.className).toContain('bg-button');
    expect(button.className).toContain('text-text-dark');
    expect(button.className).not.toContain('bg-white');
    expect(button.className).not.toContain('text-button');
    expect(button.className).not.toContain('border');
  });

  describe('Slot rendering', () => {
    it('renders icon slot content', () => {
      const { getByText } = render(IconButton, {
        slots: { icon: '<svg data-testid="icon-svg"></svg>' },
      });
      // Note: Testing for complex SVG might require more specific queries or data-testid on the slot content itself.
      // For simplicity, if the SVG was complex, we'd add a data-testid to it in the slot prop.
      // Here, we assume the string content is enough or we query by a known element if simple.
      // Using getByText might not be ideal for SVG, but if it's simple text, it's fine.
      // Let's assume for this test, the icon slot contains distinguishable text or a simple element.
      // A better way for complex HTML in slots:
      // const { container } = render(IconButton, { slots: { icon: '<div data-testid="icon-slot-content">ICON</div>' } });
      // expect(container.querySelector('[data-testid="icon-slot-content"]')).toBeInTheDocument();
      // For now, let's assume a simple text "Icon" for testing purposes or use a data-testid.
      const { container } = render(IconButton, { slots: { icon: '<span>Icon</span>' } });
      expect(container.querySelector('span')).toHaveTextContent('Icon');
    });

    it('renders text slot content', () => {
      const { getByText } = render(IconButton, {
        slots: { text: 'Click Me' },
      });
      expect(getByText('Click Me')).toBeInTheDocument();
    });

    it('renders both icon and text slot content', () => {
      const { getByText, container } = render(IconButton, {
        slots: { icon: '<i>Icon</i>', text: 'Button Text' },
      });
      expect(container.querySelector('i')).toHaveTextContent('Icon');
      expect(getByText('Button Text')).toBeInTheDocument();
    });

    it("applies 'pr-2' to icon container when text slot is also present", () => {
      const { container } = render(IconButton, {
        slots: { icon: '<span>ICON</span>', text: 'TEXT' },
      });
      const iconContainer = container.querySelector('div > div:first-child'); // The div wrapping the icon slot
      expect(iconContainer).toHaveClass('pr-2');
    });

    it("does not apply 'pr-2' to icon container when only icon slot is present", () => {
      const { container } = render(IconButton, {
        slots: { icon: '<span>ICON</span>' },
      });
      const iconContainer = container.querySelector('div > div:first-child'); // The div wrapping the icon slot
      expect(iconContainer).not.toHaveClass('pr-2');
    });
  });

  it('emits a click event when clicked', async () => {
    const handleClick = vi.fn();
    const { getByRole, component } = render(IconButton);
    component.$on('click', handleClick);

    const button = getByRole('button');
    await fireEvent.click(button);

    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
