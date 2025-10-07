import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, info) {
    // eslint-disable-next-line no-console
    console.error('UI error:', error, info);
  }

  handleReset = () => {
    try {
      window.localStorage.removeItem('fs2_token');
    } catch {}
    this.setState({ hasError: false, error: null });
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-6 text-sm text-slate-200">
          <h1 className="mb-2 text-lg font-semibold text-white">Something went wrong</h1>
          <pre className="whitespace-pre-wrap rounded bg-slate-900 p-3 text-red-300">
            {String(this.state.error)}
          </pre>
          <button
            type="button"
            onClick={this.handleReset}
            className="mt-3 rounded bg-brand px-3 py-2 text-white"
          >
            Clear session and reload
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

export default ErrorBoundary;

